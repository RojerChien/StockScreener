"""stockscreener.strategies.vcp – Volatility Contraction Pattern screener."""

from __future__ import annotations

import logging

import pandas as pd

from stockscreener.indicators.sma import calculate_sma, check_continuous_increase

logger = logging.getLogger(__name__)

__all__ = [
    "vcp_screener_strategy",
    "calculate_volatility_duration",
    "calculate_avg_volume_duration",
]

# ── VCP 預設參數 ────────────────────────────────────────────────────────────
_SMA_SHORT = 55
_SMA_MID = 144
_SMA_LONG = 233
_SMA_LONG_INCREASE_DAYS = 21
_SMA_LONG_MIN_SLOPE_PCT = 0.005   # SMA233 在 21 天內至少需上升 0.5%
_VOL_RATIO_MIN = 1.5
_MAX_VOLATILITY_8 = 0.1
_MAX_VOLUME_RATIO = 0.7

# ── Minervini 趨勢模板額外條件 ───────────────────────────────────────────────
_MIN_PRICE = 10.0            # 最低股價（設為 0 可停用）
_MIN_AVG_VOLUME_50 = 300_000  # 50 日均量下限（設為 0 可停用）
_MIN_DIST_FROM_52W_LOW = 1.30  # 收盤須至少比 52 週低點高 30%
_MAX_DIST_FROM_52W_HIGH = 0.75  # 收盤須在 52 週高點的 75% 以上


def calculate_volatility_duration(df: pd.DataFrame, end_day: int, start_day: int = 0) -> float:
    """計算指定期間的波動率。

    波動率 = (max_close / avg_close - 1) + (avg_close / min_close - 1)

    Parameters
    ----------
    df:
        含有 ``close`` 欄位的 DataFrame（最新資料在末尾）。
    end_day:
        從尾端算起的結束天數（含）。
    start_day:
        從尾端算起的開始天數，預設 0（即最近一天）。

    Returns
    -------
    float
        波動率（已四捨五入至小數點後兩位）。
    """
    hist = df.iloc[-(end_day + 1) : -(start_day) if start_day > 0 else len(df)]
    if hist.empty:
        return 0.0
    avg_close = hist["close"].mean()
    max_close = hist["close"].max()
    min_close = hist["close"].min()
    if avg_close == 0 or min_close == 0:
        return 0.0
    volatility_h = max_close / avg_close - 1
    volatility_l = avg_close / min_close - 1
    return round(volatility_h + volatility_l, 2)


def calculate_avg_volume_duration(df: pd.DataFrame, end_day: int, start_day: int = 0) -> float:
    """計算指定期間的平均成交量。

    Parameters
    ----------
    df:
        含有 ``volume`` 欄位的 DataFrame（最新資料在末尾）。
    end_day:
        從尾端算起的結束天數（含）。
    start_day:
        從尾端算起的開始天數，預設 0。

    Returns
    -------
    float
        平均成交量。
    """
    hist = df.iloc[-(end_day + 1) : -(start_day) if start_day > 0 else len(df)]
    if hist.empty:
        return 0.0
    return float(hist["volume"].mean())


def vcp_screener_strategy(ticker: str, data: pd.DataFrame) -> bool:
    """判斷股票是否符合 VCP（波動收縮型態）篩選條件。

    原始條件（Minervini VCP）：
    1. 波動率持續收縮：volatility_8 < volatility_21 < volatility_55
    2. 波動率收縮比例夠大：vol55/vol21 > 1.5 且 vol21/vol8 > 1.5
    3. 最內層波動率 < 0.1
    4. 成交量收縮：avg_volume_8 < avg_volume_55 且比例 < 0.7
    5. SMA 對齊：SMA55 > SMA144 > SMA233
    6. SMA233 近 21 天持續上升（且斜率 >= 0.5%）

    新增條件（趨勢模板 / 假訊號過濾）：
    7. 收盤價 >= 最低股價門檻（預設 $10）
    8. 50 日均量 >= 最低流動性門檻（預設 300,000）
    9. 收盤 >= 52 週低點 × 1.30（距低點至少 +30%）
    10. 收盤 >= 52 週高點 × 0.75（在高點 75% 以上）

    Parameters
    ----------
    ticker:
        股票代號（用於記錄 log）。
    data:
        含有 ``close`` 與 ``volume`` 欄位的 DataFrame。

    Returns
    -------
    bool
        符合所有 VCP 條件時回傳 ``True``。
    """
    if data.empty or len(data) < _SMA_LONG:
        logger.debug("%s: 資料不足，跳過", ticker)
        return False

    try:
        # ── 原始 VCP 條件 ────────────────────────────────────────────────────
        volatility_8 = calculate_volatility_duration(data, 8, 0)
        volatility_21 = calculate_volatility_duration(data, 21, 13)
        volatility_55 = calculate_volatility_duration(data, 55, 21)

        avg_volume_8 = calculate_avg_volume_duration(data, 8, 0)
        avg_volume_55 = calculate_avg_volume_duration(data, 55, 21)

        sma55 = calculate_sma(data, _SMA_SHORT)
        sma144 = calculate_sma(data, _SMA_MID)
        sma233 = calculate_sma(data, _SMA_LONG)

        last_sma55 = round(float(sma55.iloc[-1]), 2)
        last_sma144 = round(float(sma144.iloc[-1]), 2)
        last_sma233 = round(float(sma233.iloc[-1]), 2)

        is_continuous_increase_sma233 = check_continuous_increase(
            sma233.dropna(),
            days=_SMA_LONG_INCREASE_DAYS,
            min_slope_pct=_SMA_LONG_MIN_SLOPE_PCT,
        )

        if avg_volume_55 == 0:
            return False

        result = (
            (volatility_8 < volatility_21)
            and (volatility_21 < volatility_55)
            and (avg_volume_8 < avg_volume_55)
            and ((avg_volume_8 / avg_volume_55) < _MAX_VOLUME_RATIO)
            and ((volatility_55 / volatility_21) > _VOL_RATIO_MIN)
            and ((volatility_21 / volatility_8) > _VOL_RATIO_MIN if volatility_8 > 0 else False)
            and (volatility_8 < _MAX_VOLATILITY_8)
            and (last_sma55 > last_sma144)
            and (last_sma144 > last_sma233)
            and is_continuous_increase_sma233
        )

        if not result:
            return False

        # ── 新增條件：趨勢模板 / 假訊號過濾 ────────────────────────────────
        last_close = float(data["close"].iloc[-1])

        # 條件 7：最低股價
        if _MIN_PRICE > 0 and last_close < _MIN_PRICE:
            logger.debug("%s: 股價 %.2f 低於門檻 %.2f", ticker, last_close, _MIN_PRICE)
            return False

        # 條件 8：50 日最低均量
        if _MIN_AVG_VOLUME_50 > 0:
            avg_volume_50 = calculate_avg_volume_duration(data, 50, 0)
            if avg_volume_50 < _MIN_AVG_VOLUME_50:
                logger.debug("%s: 50日均量 %.0f 低於門檻 %.0f", ticker, avg_volume_50, _MIN_AVG_VOLUME_50)
                return False

        # 條件 9 & 10：52 週位置
        week52_data = data["close"].tail(252)
        if len(week52_data) >= 50:   # 至少需有足夠歷史
            w52_high = float(week52_data.max())
            w52_low = float(week52_data.min())
            if w52_low > 0 and last_close < w52_low * _MIN_DIST_FROM_52W_LOW:
                logger.debug(
                    "%s: 收盤 %.2f 距 52w 低點 %.2f 未達 %.0f%%",
                    ticker, last_close, w52_low, (_MIN_DIST_FROM_52W_LOW - 1) * 100,
                )
                return False
            if w52_high > 0 and last_close < w52_high * _MAX_DIST_FROM_52W_HIGH:
                logger.debug(
                    "%s: 收盤 %.2f 低於 52w 高點 %.2f 的 %.0f%%",
                    ticker, last_close, w52_high, _MAX_DIST_FROM_52W_HIGH * 100,
                )
                return False

        logger.info("%s 符合 VCP 條件", ticker)
        return True

    except Exception as exc:
        logger.error("計算 %s VCP 時發生錯誤: %s", ticker, exc)
        return False
