"""stockscreener.data.edgar – SEC EDGAR filing retrieval helpers."""

from __future__ import annotations

import logging
from typing import List, Optional

import requests
from bs4 import BeautifulSoup  # type: ignore

logger = logging.getLogger(__name__)

__all__ = [
    "get_company_filings",
    "parse_eps_from_filing",
]

_SEC_HEADERS = {
    "User-Agent": "StockScreener/1.0 (research tool)"
}


def get_company_filings(
    ticker: str,
    form_types: Optional[List[str]] = None,
    amount: int = 5,
) -> list:
    """取得指定公司的 SEC EDGAR 申報清單。

    Parameters
    ----------
    ticker:
        股票代號，例如 ``'MSFT'``。
    form_types:
        要篩選的申報類型列表，例如 ``['10-Q', '10-K']``。
        若為 ``None`` 則回傳所有類型。
    amount:
        最多回傳的申報筆數。

    Returns
    -------
    list
        申報資訊列表（dict），每筆包含 form, filingDate, reportDate, linkToFilingDetails。
    """
    try:
        from sec_edgar_py import EdgarWrapper  # type: ignore

        client = EdgarWrapper()
        filings = client.get_company_filings(ticker, form_types=form_types, amount=amount)
        return filings
    except ImportError:
        logger.warning("sec-edgar-py 未安裝，無法取得 EDGAR 申報資料")
        return []
    except Exception as exc:
        logger.error("取得 %s 的 EDGAR 資料時發生錯誤: %s", ticker, exc)
        return []


def parse_eps_from_filing(url: str) -> dict:
    """從 SEC EDGAR HTML 申報頁面解析 EPS 數值。

    Parameters
    ----------
    url:
        申報頁面的完整 URL。

    Returns
    -------
    dict
        包含 ``basic_eps`` 與 ``diluted_eps`` 的字典。
        若解析失敗則值為 ``None``。
    """
    result = {"basic_eps": None, "diluted_eps": None}

    try:
        session = requests.Session()
        response = session.get(url, headers=_SEC_HEADERS, timeout=30)
        if response.status_code != 200:
            logger.error("取得申報頁面失敗，狀態碼: %d", response.status_code)
            return result

        soup = BeautifulSoup(response.text, "lxml")

        basic_tag = soup.find(
            "ix:nonfraction",
            {
                "name": "us-gaap:EarningsPerShareBasic",
                "unitref": "U_UnitedStatesOfAmericaDollarsShare",
            },
        )
        diluted_tag = soup.find(
            "ix:nonfraction",
            {
                "name": "us-gaap:EarningsPerShareDiluted",
                "unitref": "U_UnitedStatesOfAmericaDollarsShare",
            },
        )

        if basic_tag:
            result["basic_eps"] = float(basic_tag.text)
        if diluted_tag:
            result["diluted_eps"] = float(diluted_tag.text)

    except Exception as exc:
        logger.error("解析 EPS 時發生錯誤: %s", exc)

    return result
