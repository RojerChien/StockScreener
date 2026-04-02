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
_VOL_RATIO_MIN = 1.5
_MAX_VOLATILITY_8 = 0.1
_MAX_VOLUME_RATIO = 0.7


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

    條件：
    1. 波動率持續收縮：volatility_8 < volatility_21 < volatility_55
    2. 波動率收縮比例夠大：vol55/vol21 > 1.5 且 vol21/vol8 > 1.5
    3. 最內層波動率 < 0.1
    4. 成交量收縮：avg_volume_8 < avg_volume_55 且比例 < 0.7
    5. SMA 對齊：SMA55 > SMA144 > SMA233
    6. SMA233 近 21 天持續上升

    Parameters
    ----------
    ticker:
        股票代號（用於記錄 log）。
    data:
        含有 ``close`` 與 ``volume`` 欄位的 DataFrame。

    Returns
    -------
    bool
        符合 VCP 條件時回傳 ``True``。
    """
    if data.empty or len(data) < _SMA_LONG:
        logger.debug("%s: 資料不足，跳過", ticker)
        return False

    try:
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
            sma233.dropna(), days=_SMA_LONG_INCREASE_DAYS
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

        if result:
            logger.info("%s 符合 VCP 條件", ticker)
        return result

    except Exception as exc:
        logger.error("計算 %s VCP 時發生錯誤: %s", ticker, exc)
        return False
