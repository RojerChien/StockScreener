"""stockscreener.data.russell – Russell 1000 成分股取得（iShares IWB）。

iShares Russell 1000 ETF（代號 IWB）每日公布所有持倉 CSV，
格式為多行 metadata 後接欄位標題列（Name, Ticker, Asset Class, ...），
過濾 Asset Class == "Equity" 即可取得 Russell 1000 成分股。
"""

from __future__ import annotations

import io
import logging
from typing import List

logger = logging.getLogger(__name__)

__all__ = ["get_russell1000_tickers"]

# iShares IWB 持倉 CSV 下載 URL（timestamp 參數伺服器端忽略，固定值即可）
_IWB_CSV_URL = (
    "https://www.ishares.com/us/products/239707/IWB/"
    "1467271812596.ajax?tab=all&fileType=csv"
)

_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.ishares.com/us/products/239707/",
}


def _parse_iwb_csv(text: str) -> List[str]:
    """解析 iShares IWB CSV 文字，回傳所有 Equity 類型的股票代號。

    Parameters
    ----------
    text:
        iShares CSV 原始文字（已解碼，含 BOM 或不含均可）。

    Returns
    -------
    list[str]
        股票代號列表（已去除空白，排除無效值）。
    """
    import pandas as pd

    lines = text.splitlines()

    # 找到含欄位標題的起始行（以 "Name" 開頭）
    start_idx: int | None = None
    for i, line in enumerate(lines):
        cleaned = line.strip().strip("\ufeff").strip('"')
        if cleaned.startswith("Name"):
            start_idx = i
            break

    if start_idx is None:
        raise ValueError("無法識別 iShares IWB CSV 格式（找不到 Name 欄位標題）")

    # 找到資料結束行：遇到空行或無效行時停止
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        # 空行或全逗號行（CSV footer）視為結束
        if not stripped or all(c in (",", '"', " ") for c in stripped):
            end_idx = i
            break

    csv_block = "\n".join(lines[start_idx:end_idx])
    df = pd.read_csv(io.StringIO(csv_block))

    # 過濾股票類型（排除債券、現金等非股票持倉）
    if "Asset Class" in df.columns:
        df = df[df["Asset Class"].str.strip() == "Equity"]

    if "Ticker" not in df.columns:
        raise ValueError("CSV 中找不到 Ticker 欄位")

    tickers = [
        t.strip()
        for t in df["Ticker"].dropna().astype(str)
        if t.strip() and t.strip() not in ("-", "nan")
    ]
    return tickers


def get_russell1000_tickers(url: str = _IWB_CSV_URL) -> List[str]:
    """從 iShares IWB ETF 持倉 CSV 取得 Russell 1000 成分股代號。

    Parameters
    ----------
    url:
        iShares IWB CSV 下載 URL，預設使用官方固定連結。

    Returns
    -------
    list[str]
        Russell 1000 成分股股票代號列表（約 1000 支）。

    Raises
    ------
    ConnectionError
        無法連線至 iShares 時拋出。
    ValueError
        CSV 格式無法解析時拋出。
    """
    import requests  # type: ignore

    logger.info("從 iShares IWB 取得 Russell 1000 成分股...")
    try:
        resp = requests.get(url, headers=_REQUEST_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        raise ConnectionError(
            f"無法取得 iShares IWB 持倉資料（{exc}）\n"
            "請確認網路連線正常後再試。"
        ) from exc

    # 處理 UTF-8 BOM
    text = resp.content.decode("utf-8-sig")
    tickers = _parse_iwb_csv(text)

    logger.info("取得 Russell 1000 成分股共 %d 支", len(tickers))
    return tickers
