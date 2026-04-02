"""stockscreener.indicators.rsi – Relative Strength Index."""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["calculate_rsi"]

_DEFAULT_PERIOD = 14


def calculate_rsi(data: pd.DataFrame, period: int = _DEFAULT_PERIOD) -> pd.Series:
    """計算 RSI（相對強弱指標）。

    使用簡單滾動平均（SMA）計算 avg_gain 與 avg_loss，與原始
    main_screener.py 保持一致。

    Parameters
    ----------
    data:
        含有 ``close`` 欄位的 DataFrame。
    period:
        RSI 計算週期，預設 14。

    Returns
    -------
    pd.Series
        RSI 序列（0–100 之間）。
    """
    delta = data["close"].diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
