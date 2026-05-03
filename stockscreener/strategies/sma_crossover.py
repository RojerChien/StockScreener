"""stockscreener.strategies.sma_crossover – SMA crossover buy/sell signal generator."""

from __future__ import annotations

import logging
from typing import List, Tuple

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["sma_crossover_signals"]

# ── 預設 SMA 參數（對應 Backtest_pyramid_record.py）─────────────────────────
_SMA_FAST = 21
_SMA_SLOW = 55
_SMA_TREND = 155


def sma_crossover_signals(
    data: pd.DataFrame,
    fast: int = _SMA_FAST,
    slow: int = _SMA_SLOW,
    trend: int = _SMA_TREND,
) -> Tuple[List, List]:
    """產生 SMA 交叉的買進 / 賣出訊號列表。

    買進條件（同時滿足）：
    - SMA_fast 從下方穿越 SMA_slow（黃金交叉）
    - close > SMA_fast > SMA_slow > SMA_trend
    - 三條 SMA 都在上升（今日 > 昨日）
    - 目前尚未持有部位

    賣出條件：
    - close < SMA_fast，且目前持有部位

    Parameters
    ----------
    data:
        含有 ``close`` 欄位的 DataFrame。
    fast:
        快速 SMA 視窗，預設 21。
    slow:
        慢速 SMA 視窗，預設 55。
    trend:
        趨勢 SMA 視窗，預設 155。

    Returns
    -------
    tuple[list, list]
        (buy_signals, sell_signals) – 各為日期索引列表。
        兩個列表長度相等（未平倉訊號已裁切）。
    """
    df = data.copy()
    df[f"sma{fast}"] = df["close"].rolling(window=fast).mean()
    df[f"sma{slow}"] = df["close"].rolling(window=slow).mean()
    df[f"sma{trend}"] = df["close"].rolling(window=trend).mean()

    buy_signals: List = []
    sell_signals: List = []
    position = False

    for i in range(1, len(df)):
        sma_fast_prev = df[f"sma{fast}"].iloc[i - 1]
        sma_slow_prev = df[f"sma{slow}"].iloc[i - 1]
        sma_fast_cur = df[f"sma{fast}"].iloc[i]
        sma_slow_cur = df[f"sma{slow}"].iloc[i]
        sma_trend_cur = df[f"sma{trend}"].iloc[i]
        sma_fast_prev_day = df[f"sma{fast}"].iloc[i - 1]
        sma_slow_prev_day = df[f"sma{slow}"].iloc[i - 1]
        sma_trend_prev_day = df[f"sma{trend}"].iloc[i - 1]
        close_cur = df["close"].iloc[i]

        # 任何一個 SMA 為 NaN 則跳過
        if pd.isna(sma_fast_cur) or pd.isna(sma_slow_cur) or pd.isna(sma_trend_cur):
            continue

        # 買進條件
        sma_cross = sma_fast_prev < sma_slow_prev and sma_fast_cur > sma_slow_cur
        sma_conditions = close_cur > sma_fast_cur > sma_slow_cur > sma_trend_cur
        sma_increasing = (
            sma_fast_cur > sma_fast_prev_day
            and sma_slow_cur > sma_slow_prev_day
            and sma_trend_cur > sma_trend_prev_day
        )

        if sma_cross and sma_conditions and sma_increasing and not position:
            buy_signals.append(df.index[i])
            position = True

        # 賣出條件
        elif close_cur < sma_fast_cur and position:
            sell_signals.append(df.index[i])
            position = False

    # 確保買賣訊號數量一致
    if len(buy_signals) > len(sell_signals):
        buy_signals.pop()

    logger.debug(
        "SMA 交叉訊號：買進 %d 次，賣出 %d 次", len(buy_signals), len(sell_signals)
    )
    return buy_signals, sell_signals
