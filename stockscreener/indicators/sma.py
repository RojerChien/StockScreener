"""stockscreener.indicators.sma – Simple Moving Average."""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["calculate_sma", "check_continuous_increase"]


def calculate_sma(data: pd.DataFrame, window: int) -> pd.Series:
    """計算 SMA（簡單移動平均）。

    Parameters
    ----------
    data:
        含有 ``close`` 欄位的 DataFrame。
    window:
        滾動視窗大小（天數）。

    Returns
    -------
    pd.Series
        SMA 序列。
    """
    return data["close"].rolling(window=window).mean()


def check_continuous_increase(series: pd.Series, days: int) -> bool:
    """判斷序列在最後 *days* 天是否持續上升。

    Parameters
    ----------
    series:
        已去除 NaN 的 SMA 序列。
    days:
        要檢查的天數。

    Returns
    -------
    bool
        若最後 *days* 天單調遞增則回傳 ``True``，否則回傳 ``False``。
    """
    if len(series) < days:
        return False
    last_n = series.tail(days)
    return bool(last_n.is_monotonic_increasing)
