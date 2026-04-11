"""stockscreener.strategies.vcp_signal – VCP 突破訊號產生器（供回測引擎使用）。

採用向量化預計算（O(n)）產生 VCP 條件布林遮罩，
避免逐日呼叫 vcp_screener_strategy 造成的 O(n²) 效能問題。

進場條件（同時滿足）：
1. 前一日 VCP 條件通過（向量化預計算）
2. 收盤 > 前 breakout_window 日最高收盤（突破）
3. 今日成交量 > 50 日均量 × volume_multiplier（量能確認）

出場條件（任一滿足）：
- 收盤 < 進場價 × (1 - stop_loss_pct)    ← 停損
- 收盤 > 進場價 × (1 + profit_target_pct)  ← 獲利了結
- 收盤 < SMA21                              ← 趨勢破壞
"""

from __future__ import annotations

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["vcp_breakout_signals"]

# ── 與 vcp.py 保持一致的篩選常數 ──────────────────────────────────────────────
_VOL_RATIO_MIN = 1.5
_MAX_VOLATILITY_8 = 0.1
_MAX_VOLUME_RATIO = 0.7
_SMA_LONG_MIN_SLOPE_PCT = 0.005   # SMA233 21 天累計斜率下限
_MIN_PRICE = 10.0
_MIN_AVG_VOLUME_50 = 300_000
_MIN_DIST_FROM_52W_LOW = 1.30
_MAX_DIST_FROM_52W_HIGH = 0.75

# ── 突破訊號預設參數 ──────────────────────────────────────────────────────────
_STOP_LOSS_PCT = 0.07
_PROFIT_TARGET_PCT = 0.25
_VOLUME_MULTIPLIER = 1.3
_BREAKOUT_WINDOW = 55


def _vol_series(close: pd.Series, shift: int, window: int) -> pd.Series:
    """向量化計算非重疊視窗波動率。

    對應 calculate_volatility_duration 的向量化版本：

    - shift=0,  window=9  → end_day=8,  start_day=0  （最近 9 天）
    - shift=14, window=9  → end_day=21, start_day=13 （14–22 天前）
    - shift=22, window=35 → end_day=55, start_day=21 （22–56 天前）

    每種組合的推導：對位置 i 而言，
    ``df.iloc[-(end_day+1):-(start_day)]`` 等同於
    ``close.shift(start_day+1).rolling(end_day-start_day+1)``。
    """
    s = close.shift(shift) if shift > 0 else close
    roll = s.rolling(window, min_periods=window)
    avg = roll.mean()
    mx = roll.max()
    mn = roll.min()
    with np.errstate(divide="ignore", invalid="ignore"):
        v = (mx / avg - 1) + (avg / mn - 1)
    return v.fillna(0.0)


def _precompute_vcp_mask(data: pd.DataFrame) -> pd.Series:
    """向量化計算每個交易日是否通過所有 VCP 條件，回傳 bool Series。

    此函式是 ``vcp_screener_strategy`` 的向量化等價版本。
    結果可直接用 ``.shift(1)`` 取前日訊號，使整體信號生成維持 O(n)。
    """
    close = data["close"]
    volume = data["volume"]

    # ── 波動率（三段非重疊視窗）────────────────────────────────────────────
    vol8 = _vol_series(close, shift=0, window=9)     # 最近 9 天
    vol21 = _vol_series(close, shift=14, window=9)   # 14–22 天前（9 天）
    vol55 = _vol_series(close, shift=22, window=35)  # 22–56 天前（35 天）

    # ── 成交量（非重疊視窗）────────────────────────────────────────────────
    avg_vol8 = volume.rolling(9, min_periods=9).mean()
    avg_vol55 = volume.shift(22).rolling(35, min_periods=35).mean()

    # ── SMA ────────────────────────────────────────────────────────────────
    sma55 = close.rolling(55, min_periods=55).mean()
    sma144 = close.rolling(144, min_periods=144).mean()
    sma233 = close.rolling(233, min_periods=233).mean()

    # SMA233：21 天單調遞增，且累計漲幅 >= _SMA_LONG_MIN_SLOPE_PCT
    sma233_monotone = (sma233.diff(1) >= 0).astype(float)
    sma233_diff_ok = (
        sma233_monotone.rolling(21, min_periods=21).min().fillna(0).astype(bool)
    )
    sma233_slope_ok = (sma233 / sma233.shift(21) - 1) >= _SMA_LONG_MIN_SLOPE_PCT

    # ── 50 日均量（條件 8）────────────────────────────────────────────────
    avg_vol50 = volume.rolling(51, min_periods=51).mean()

    # ── 52 週高低點（條件 9 & 10，至少需 50 天資料）──────────────────────
    w52_high = close.rolling(252, min_periods=50).max()
    w52_low = close.rolling(252, min_periods=50).min()

    # 除數保護
    safe_vol21 = vol21.where(vol21 > 0)
    safe_vol8 = vol8.where(vol8 > 0)
    safe_avg_vol55 = avg_vol55.where(avg_vol55 > 0)
    safe_w52_low = w52_low.where(w52_low > 0)
    safe_w52_high = w52_high.where(w52_high > 0)

    mask = (
        (vol8 < vol21)
        & (vol21 < vol55)
        & (avg_vol8 < avg_vol55)
        & ((avg_vol8 / safe_avg_vol55) < _MAX_VOLUME_RATIO)
        & ((vol55 / safe_vol21) > _VOL_RATIO_MIN)
        & ((vol21 / safe_vol8) > _VOL_RATIO_MIN)
        & (vol8 < _MAX_VOLATILITY_8)
        & (sma55 > sma144)
        & (sma144 > sma233)
        & sma233_diff_ok
        & sma233_slope_ok
        & (close >= _MIN_PRICE)
        & (avg_vol50 >= _MIN_AVG_VOLUME_50)
        & (close >= safe_w52_low * _MIN_DIST_FROM_52W_LOW)
        & (close >= safe_w52_high * _MAX_DIST_FROM_52W_HIGH)
    ).fillna(False)

    return mask


def vcp_breakout_signals(
    data: pd.DataFrame,
    stop_loss_pct: float = _STOP_LOSS_PCT,
    profit_target_pct: float = _PROFIT_TARGET_PCT,
    volume_multiplier: float = _VOLUME_MULTIPLIER,
    breakout_window: int = _BREAKOUT_WINDOW,
) -> Tuple[List, List]:
    """產生 VCP 突破的買進 / 賣出訊號列表。

    Parameters
    ----------
    data:
        含有 ``close``、``volume`` 欄位的 DataFrame（DatetimeIndex，最新資料在末尾）。
    stop_loss_pct:
        停損比例，預設 0.07（7%）。
    profit_target_pct:
        獲利了結比例，預設 0.25（25%）。
    volume_multiplier:
        進場當日量需超過 50 日均量的倍數，預設 1.3。
    breakout_window:
        突破參考的歷史高點天數，預設 55。

    Returns
    -------
    tuple[list, list]
        (buy_signals, sell_signals) – 各為日期索引列表，長度相等。
    """
    if data.empty or len(data) < 233:
        return [], []

    # ── 向量化預計算（O(n)）────────────────────────────────────────────────
    vcp_mask = _precompute_vcp_mask(data)
    # 使用前一日訊號避免前瞻偏差
    vcp_prev = vcp_mask.shift(1).fillna(False)

    # 突破前高（以前一日為截止點）
    prev_high = data["close"].shift(1).rolling(breakout_window, min_periods=1).max()

    # 50 日均量（以前一日為截止點）
    avg_vol_50 = data["volume"].shift(1).rolling(50, min_periods=1).mean()

    # SMA21（趨勢破壞出場）
    sma21 = data["close"].rolling(21, min_periods=21).mean()

    buy_signals: List = []
    sell_signals: List = []
    position = False
    entry_price = 0.0

    for i in range(len(data)):
        if i < 233:
            continue

        date_cur = data.index[i]
        close_cur = float(data["close"].iloc[i])

        # ── 持倉中：檢查出場條件 ──────────────────────────────────────────
        if position:
            sma21_cur = sma21.iloc[i]

            if close_cur < entry_price * (1 - stop_loss_pct):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 停損出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

            if close_cur > entry_price * (1 + profit_target_pct):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 獲利出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

            if not pd.isna(sma21_cur) and close_cur < float(sma21_cur):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 趨勢破壞出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

        # ── 無持倉：檢查進場條件 ────────────────────────────────────────
        else:
            if not bool(vcp_prev.iloc[i]):
                continue

            ph = prev_high.iloc[i]
            if pd.isna(ph) or close_cur <= float(ph):
                continue

            av = avg_vol_50.iloc[i]
            if (
                not pd.isna(av)
                and float(av) > 0
                and float(data["volume"].iloc[i]) < float(av) * volume_multiplier
            ):
                continue

            buy_signals.append(date_cur)
            position = True
            entry_price = close_cur
            logger.debug("VCP 進場 @ %s, 價格 %.2f", date_cur, close_cur)

    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    logger.debug("VCP 突破訊號：買進 %d 次，賣出 %d 次", len(buy_signals), len(sell_signals))
    return buy_signals, sell_signals
