"""stockscreener.strategies.vcp_signal – VCP 突破訊號產生器（供回測引擎使用）。

進場條件（同時滿足）：
1. 當日 VCP 篩選通過（`vcp_screener_strategy`）
2. 收盤 > 前 55 日最高收盤（突破）
3. 今日成交量 > 50 日均量 × 1.3（量能確認）

出場條件（任一滿足）：
- 收盤 < 進場價 × (1 - stop_loss_pct)   ← 停損
- 收盤 > 進場價 × (1 + profit_target_pct) ← 獲利了結
- 收盤 < SMA21                            ← 趨勢破壞
"""

from __future__ import annotations

import logging
from typing import List, Tuple

import pandas as pd

from stockscreener.strategies.vcp import vcp_screener_strategy

logger = logging.getLogger(__name__)

__all__ = ["vcp_breakout_signals"]

# ── 預設參數 ──────────────────────────────────────────────────────────────────
_STOP_LOSS_PCT = 0.07          # 停損：跌破進場價 7%
_PROFIT_TARGET_PCT = 0.25      # 獲利了結：漲幅達 25%
_VOLUME_MULTIPLIER = 1.3       # 進場當日量 > 50 日均量 × 1.3
_BREAKOUT_WINDOW = 55          # 突破前 N 日高點


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
    buy_signals: List = []
    sell_signals: List = []
    position = False
    entry_price = 0.0

    # 預先計算 SMA21（用於趨勢破壞出場）
    sma21 = data["close"].rolling(window=21).mean()

    for i in range(1, len(data)):
        # 確保有足夠資料供 VCP 計算（至少需要 233 天）
        if i < 233:
            continue

        close_cur = float(data["close"].iloc[i])
        date_cur = data.index[i]

        # ── 持倉中：檢查出場條件 ──────────────────────────────────────────
        if position:
            sma21_cur = sma21.iloc[i]

            # 出場：停損
            if close_cur < entry_price * (1 - stop_loss_pct):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 停損出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

            # 出場：獲利了結
            if close_cur > entry_price * (1 + profit_target_pct):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 獲利出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

            # 出場：趨勢破壞（收盤跌破 SMA21）
            if not pd.isna(sma21_cur) and close_cur < float(sma21_cur):
                sell_signals.append(date_cur)
                position = False
                logger.debug("VCP 趨勢破壞出場 @ %s, 價格 %.2f", date_cur, close_cur)
                continue

        # ── 無持倉：檢查進場條件 ────────────────────────────────────────
        else:
            slice_df = data.iloc[: i + 1]

            # 條件 1：VCP 篩選通過（使用迄今資料）
            if not vcp_screener_strategy("_bt_", slice_df):
                continue

            # 條件 2：收盤突破前 breakout_window 日最高收盤
            # 取 i 之前（不含今日）的 breakout_window 個收盤
            start_idx = max(0, i - breakout_window)
            prev_high = float(data["close"].iloc[start_idx:i].max())
            if close_cur <= prev_high:
                continue

            # 條件 3：今日量 > 50 日均量 × volume_multiplier
            vol_start = max(0, i - 50)
            avg_vol_50 = float(data["volume"].iloc[vol_start:i].mean())
            if avg_vol_50 > 0 and float(data["volume"].iloc[i]) < avg_vol_50 * volume_multiplier:
                continue

            buy_signals.append(date_cur)
            position = True
            entry_price = close_cur
            logger.debug("VCP 進場 @ %s, 價格 %.2f", date_cur, close_cur)

    # 若最後仍持倉，裁切最後一個未平倉買進訊號
    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    logger.debug("VCP 突破訊號：買進 %d 次，賣出 %d 次", len(buy_signals), len(sell_signals))
    return buy_signals, sell_signals
