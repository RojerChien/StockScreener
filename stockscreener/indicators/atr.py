"""stockscreener.indicators.atr – Average True Range."""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["calculate_atr"]

_DEFAULT_PERIOD = 14


def calculate_atr(data: pd.DataFrame, period: int = _DEFAULT_PERIOD) -> pd.Series:
    """計算 ATR（平均真實範圍）。

    True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
    ATR = rolling_mean(True Range, period)

    Parameters
    ----------
    data:
        含有 ``high``、``low``、``close`` 欄位的 DataFrame。
    period:
        ATR 計算週期，預設 14。

    Returns
    -------
    pd.Series
        ATR 序列。
    """
    high_low = data["high"] - data["low"]
    high_close = np.abs(data["high"] - data["close"].shift())
    low_close = np.abs(data["low"] - data["close"].shift())

    true_range = pd.DataFrame(
        {"hl": high_low, "hc": high_close, "lc": low_close}
    ).max(axis=1)

    atr = true_range.rolling(window=period).mean()
    return atr
