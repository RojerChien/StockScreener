"""stockscreener.data.finviz – FinViz screener wrapper."""

from __future__ import annotations

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

__all__ = ["get_finviz_screener_tickers"]

# 預設篩選條件（對應原始 main_screener.py）
_DEFAULT_FILTERS: Dict[str, str] = {
    "20-Day Simple Moving Average": "SMA20 above SMA50",
    "50-Day Simple Moving Average": "SMA50 above SMA200",
    "Average Volume": "Over 100K",
    "Price": "Over $3",
    "EPS growthpast 5 years": "Positive (>0%)",
    "Change": "Up 2%",
}


def get_finviz_screener_tickers(filters_dict: Dict[str, str] | None = None) -> List[str]:
    """從 FinViz Screener 取得符合條件的股票代號列表。

    Parameters
    ----------
    filters_dict:
        FinViz 篩選條件字典。若為 ``None`` 則使用預設條件。

    Returns
    -------
    list[str]
        股票代號列表。
    """
    from finvizfinance.screener.overview import Overview  # type: ignore

    if filters_dict is None:
        filters_dict = _DEFAULT_FILTERS

    logger.info("開始取得 FinViz Screener 股票代號")

    foverview = Overview()
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.screener_view()

    if df is None or df.empty:
        logger.warning("FinViz Screener 未回傳任何資料")
        return []

    tickers = df["Ticker"].tolist()
    logger.info("FinViz Screener 取得 %d 檔股票", len(tickers))
    return tickers
