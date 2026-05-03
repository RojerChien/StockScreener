"""stockscreener.data.yahoo – Yahoo Finance / yahooquery data fetching."""

from __future__ import annotations

import logging
import time
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = [
    "get_yq_historical_data",
    "sel_yq_historical_data",
    "normalize_columns",
]

# yfinance 下載時欄位名稱為首字母大寫，統一轉換為小寫
_COLUMN_MAP = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
    "Adj Close": "adj_close",
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """將 DataFrame 欄位名稱統一轉為小寫（yfinance → 內部標準）。"""
    rename = {k: v for k, v in _COLUMN_MAP.items() if k in df.columns}
    if rename:
        df = df.rename(columns=rename)
    # 若欄位已是小寫則直接返回
    return df


def get_yq_historical_data(ticker_list: List[str]) -> pd.DataFrame:
    """以非同步模式批次下載歷史 OHLCV 資料（yahooquery）。

    Parameters
    ----------
    ticker_list:
        股票代號列表，例如 ``['AAPL', 'TSLA']``。

    Returns
    -------
    pd.DataFrame
        MultiIndex DataFrame，第一層為 ticker，第二層為日期。
    """
    from yahooquery import Ticker  # type: ignore

    logger.info("開始下載 %d 檔股票歷史資料", len(ticker_list))
    start = time.time()

    try:
        ticker = Ticker(ticker_list, asynchronous=True)
        data_all = ticker.history(period="3y", interval="1d")
    except Exception as exc:
        raise ConnectionError(
            f"無法連線至 Yahoo Finance（{exc}）\n"
            "請確認網路連線正常，或稍後再試。"
        ) from exc

    elapsed = round(time.time() - start, 2)
    logger.info("資料下載完成，耗時 %s 秒", elapsed)
    return data_all


def sel_yq_historical_data(data_all: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """從批次下載結果中擷取單一股票的 DataFrame。

    Parameters
    ----------
    data_all:
        :func:`get_yq_historical_data` 的回傳值（MultiIndex）。
    ticker:
        目標股票代號。

    Returns
    -------
    pd.DataFrame
        單一股票的歷史資料（空 DataFrame 表示找不到）。
    """
    if isinstance(data_all.index, pd.MultiIndex):
        if ticker in data_all.index.get_level_values(0):
            return data_all.loc[ticker].copy()
    logger.debug("找不到 %s 的資料（Yahoo Finance 無此代號的歷史資料）", ticker)
    return pd.DataFrame()
