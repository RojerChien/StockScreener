"""stockscreener.data.ptp – PTP (Publicly Traded Partnership) ticker scraper."""

from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)

__all__ = ["get_ptp_tickers", "remove_ptp_tickers"]

_DEFAULT_URL1 = "https://help.zh-tw.firstrade.com/article/841-new-1446-f-regulations"
_DEFAULT_URL2 = "https://www.itigerup.com/bulletin/ptp"


def get_ptp_tickers(
    url1: str = _DEFAULT_URL1,
    url2: str = _DEFAULT_URL2,
) -> List[str]:
    """爬取兩個網站取得 PTP 股票代號列表，合併後去重。

    Parameters
    ----------
    url1:
        Firstrade 的 PTP 清單頁面 URL。
    url2:
        itigerup 的 PTP 清單頁面 URL。

    Returns
    -------
    list[str]
        不重複的 PTP 股票代號列表。
    """
    import requests  # type: ignore
    from bs4 import BeautifulSoup  # type: ignore

    ptp_lists: List[str] = []

    # --- 第一個網站 ---
    try:
        response1 = requests.get(url1, timeout=15)
        soup1 = BeautifulSoup(response1.content, "html.parser")
        table1 = soup1.find("table", {"width": "100%"})
        if table1:
            tbody1 = table1.find("tbody")
            if tbody1:
                rows1 = tbody1.find_all("tr")
                for row in rows1:
                    cols = row.find_all("td")
                    if len(cols) == 3:
                        symbol = cols[2].get_text().strip()
                        if symbol:
                            ptp_lists.append(symbol)
    except Exception as exc:
        logger.warning("無法爬取第一個 PTP 網站 (%s): %s", url1, exc)

    # --- 第二個網站 ---
    try:
        response2 = requests.get(url2, timeout=15)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        table2 = soup2.find("table", {"class": "table"})
        if table2:
            rows2 = table2.find_all("tr")
            for row in rows2:
                code = row.find("td")
                if code:
                    ticker = code.text.strip()
                    if ticker:
                        ptp_lists.append(ticker)
    except Exception as exc:
        logger.warning("無法爬取第二個 PTP 網站 (%s): %s", url2, exc)

    # 合併兩個列表並去重
    ptp_lists = list(set(ptp_lists))
    logger.info("共取得 %d 個 PTP 股票代號", len(ptp_lists))
    return ptp_lists


def remove_ptp_tickers(tickers: List[str], ptp_tickers: List[str]) -> List[str]:
    """從股票列表中移除 PTP 股票。

    Parameters
    ----------
    tickers:
        原始股票代號列表。
    ptp_tickers:
        PTP 股票代號列表（由 :func:`get_ptp_tickers` 取得）。

    Returns
    -------
    list[str]
        去除 PTP 後的股票代號列表。
    """
    ptp_set = set(ptp_tickers)
    us_ptp = [x for x in tickers if x in ptp_set]
    non_ptp = [x for x in tickers if x not in ptp_set]
    logger.info("已移除 %d 個 PTP 股票: %s", len(us_ptp), us_ptp)
    return non_ptp
