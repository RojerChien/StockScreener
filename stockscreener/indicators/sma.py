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


def check_continuous_increase(
    series: pd.Series, days: int, min_slope_pct: float = 0.0
) -> bool:
    """判斷序列在最後 *days* 天是否持續上升。

    Parameters
    ----------
    series:
        已去除 NaN 的 SMA 序列。
    days:
        要檢查的天數。
    min_slope_pct:
        最小斜率要求：最後一值需比第一值高出此比例（例如 0.005 = 0.5%）。
        預設 0.0 表示只要求單調遞增（允許持平）。

    Returns
    -------
    bool
        若最後 *days* 天單調遞增（且符合最小斜率要求）則回傳 ``True``。
    """
    if len(series) < days:
        return False
    last_n = series.tail(days)
    if not last_n.is_monotonic_increasing:
        return False
    if min_slope_pct > 0:
        first_val = float(last_n.iloc[0])
        last_val = float(last_n.iloc[-1])
        if first_val == 0:
            return False
        return last_val > first_val * (1 + min_slope_pct)
    return True
