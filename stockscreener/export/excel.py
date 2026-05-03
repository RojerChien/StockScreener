"""stockscreener.export.excel – Excel export helpers (openpyxl)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["export_tickers_to_excel", "export_results_to_excel"]


def export_tickers_to_excel(
    tickers: List[str],
    output_path: str | Path = "tickers.xlsx",
    sheet_name: str = "Tickers",
) -> Path:
    """將股票代號列表匯出為 Excel 檔案。

    Parameters
    ----------
    tickers:
        股票代號列表。
    output_path:
        輸出 Excel 檔案路徑，預設 ``tickers.xlsx``。
    sheet_name:
        工作表名稱，預設 ``'Tickers'``。

    Returns
    -------
    Path
        已儲存的 Excel 檔案路徑。
    """
    output_path = Path(output_path)
    df = pd.DataFrame(tickers, columns=["Ticker"])
    df.to_excel(output_path, sheet_name=sheet_name, index=False)
    logger.info("股票代號已匯出至: %s (%d 筆)", output_path, len(tickers))
    return output_path


def export_results_to_excel(
    df: pd.DataFrame,
    output_path: str | Path = "results.xlsx",
    sheet_name: str = "Results",
    index: bool = False,
) -> Path:
    """將 DataFrame 結果匯出為 Excel 檔案。

    Parameters
    ----------
    df:
        要匯出的 DataFrame。
    output_path:
        輸出 Excel 檔案路徑，預設 ``results.xlsx``。
    sheet_name:
        工作表名稱，預設 ``'Results'``。
    index:
        是否匯出 DataFrame 索引，預設 ``False``。

    Returns
    -------
    Path
        已儲存的 Excel 檔案路徑。
    """
    output_path = Path(output_path)
    df.to_excel(output_path, sheet_name=sheet_name, index=index)
    logger.info("結果已匯出至: %s (%d 列)", output_path, len(df))
    return output_path
