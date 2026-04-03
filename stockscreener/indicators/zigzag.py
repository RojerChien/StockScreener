"""stockscreener.indicators.zigzag – ZigZag indicator using ATR-derived window."""

from __future__ import annotations

import logging
from typing import List

import numpy as np
import pandas as pd

from .atr import calculate_atr

logger = logging.getLogger(__name__)

__all__ = ["calculate_zigzag"]


def _filter_and_order(values: pd.DataFrame, percentage: float) -> List:
    """確保波峰與波谷交替出現，並按最小相對差異過濾。

    Parameters
    ----------
    values:
        含有 ``date`` 與 ``price`` 欄位的 DataFrame，已按日期排序。
    percentage:
        相鄰波峰/波谷的最小相對差異（例如 0.08 = 8%）。

    Returns
    -------
    list
        過濾後的 row 物件列表。
    """
    filtered_values = [values.iloc[0]]
    for i in range(1, len(values)):
        relative_difference = (
            np.abs(values.iloc[i].price - filtered_values[-1].price)
            / filtered_values[-1].price
        )
        if relative_difference > percentage:
            # 確保波峰接著波谷，或波谷接著波峰
            if len(filtered_values) >= 2 and (
                values.iloc[i].price > filtered_values[-1].price
            ) == (filtered_values[-1].price > filtered_values[-2].price):
                del filtered_values[-1]
            filtered_values.append(values.iloc[i])
    return filtered_values


def calculate_zigzag(
    data: pd.DataFrame,
    atr_multiplier: float = 2.5,
    min_percentage: float = 0.08,
    atr_period: int = 14,
) -> pd.DataFrame:
    """計算 ZigZag 線資料點。

    使用 ATR 決定滾動視窗大小：
    ``window_size = ceil(atr.mean() * atr_multiplier)``

    Parameters
    ----------
    data:
        含有 ``high``、``low``、``close`` 欄位的 DataFrame（DatetimeIndex）。
    atr_multiplier:
        ATR 乘數，用於計算滾動視窗大小，預設 2.5。
    min_percentage:
        波峰/波谷之間的最小相對差異，預設 0.08（8%）。
    atr_period:
        ATR 計算週期，預設 14。

    Returns
    -------
    pd.DataFrame
        含有 ``price`` 欄位的 DataFrame，索引為日期（ZigZag 轉折點）。
    """
    if data.empty or len(data) < atr_period + 1:
        return pd.DataFrame(columns=["price"])

    atr = calculate_atr(data, period=atr_period)
    atr_mean = atr.mean()
    if np.isnan(atr_mean) or atr_mean == 0:
        return pd.DataFrame(columns=["price"])
    window_size = int(np.ceil(atr_mean * atr_multiplier))
    if window_size < 2:
        window_size = 2
    logger.debug("ZigZag window_size: %d", window_size)

    # 找到波峰
    data_high_rolling_max = data["high"].rolling(window=window_size, center=True).max()
    peak_indexes = data["high"] == data_high_rolling_max

    # 找到波谷
    data_low_rolling_min = data["low"].rolling(window=window_size, center=True).min()
    valley_indexes = data["low"] == data_low_rolling_min

    df_peaks = pd.DataFrame(
        {"date": data["high"].index[peak_indexes], "price": data["high"][peak_indexes]}
    )
    df_valleys = pd.DataFrame(
        {"date": data["low"].index[valley_indexes], "price": data["low"][valley_indexes]}
    )

    df_peaks_valleys = (
        pd.concat([df_peaks, df_valleys], axis=0, ignore_index=True, sort=True)
        .sort_values(by=["date"])
        .reset_index(drop=True)
    )

    if df_peaks_valleys.empty:
        return pd.DataFrame(columns=["price"])

    ordered = _filter_and_order(df_peaks_valleys, min_percentage)

    filtered_prices = pd.Series(
        [x.price for x in ordered],
        index=[x.date for x in ordered],
    )
    zigzag = pd.DataFrame(filtered_prices, columns=["price"])
    zigzag.index = pd.to_datetime(zigzag.index)
    return zigzag
