"""stockscreener.indicators.vwap – Volume-Weighted Average Price."""

from __future__ import annotations

import logging
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["calculate_vwap", "add_all_vwaps"]

# 預設 VWAP 計算視窗（對應原始 main_screener.py）
_DEFAULT_WINDOWS: List[int] = [5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]


def calculate_vwap(df: pd.DataFrame, window: int, price_col: str = "close") -> pd.DataFrame:
    """計算並將 VWAP 欄位加入 DataFrame。

    VWPrice = close × volume（或指定欄位）
    VWAP = rolling_sum(VWPrice, window) / rolling_sum(volume, window)

    Parameters
    ----------
    df:
        含有 ``close``（或 *price_col*）及 ``volume`` 欄位的 DataFrame。
    window:
        滾動視窗大小（天數）。
    price_col:
        計算 VWAP 時使用的價格欄位，預設為 ``'close'``。

    Returns
    -------
    pd.DataFrame
        原 DataFrame 加入 ``VWPrice`` 與 ``vwap{window}`` 欄位後的結果。
    """
    df = df.copy()
    df["VWPrice"] = df[price_col] * df["volume"]
    df[f"vwap{window}"] = (
        df["VWPrice"].rolling(window=window).sum()
        / df["volume"].rolling(window=window).sum()
    )
    return df


def add_all_vwaps(
    df: pd.DataFrame,
    windows: List[int] | None = None,
    price_col: str = "close",
) -> pd.DataFrame:
    """批次計算多個 VWAP 視窗，並一次加入 DataFrame。

    Parameters
    ----------
    df:
        含有 ``close``（或 *price_col*）及 ``volume`` 欄位的 DataFrame。
    windows:
        VWAP 視窗列表，預設為 :data:`_DEFAULT_WINDOWS`。
    price_col:
        計算 VWAP 時使用的價格欄位。

    Returns
    -------
    pd.DataFrame
        加入所有 ``vwap{n}`` 欄位的 DataFrame。
    """
    if windows is None:
        windows = _DEFAULT_WINDOWS

    df = df.copy()
    # 只需計算一次 VWPrice
    df["VWPrice"] = df[price_col] * df["volume"]

    for w in windows:
        df[f"vwap{w}"] = (
            df["VWPrice"].rolling(window=w).sum()
            / df["volume"].rolling(window=w).sum()
        )

    logger.debug("已計算 %d 個 VWAP 視窗: %s", len(windows), windows)
    return df
