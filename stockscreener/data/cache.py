"""stockscreener.data.cache – simple on-disk DataFrame cache (Parquet)."""

from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["cache_key", "read_cache", "write_cache"]

_DEFAULT_CACHE_DIR = Path(".cache")


def cache_key(tickers: List[str], period: str = "3y", interval: str = "1d") -> str:
    """以 ticker 列表、period 與 interval 產生確定性的快取鍵值。"""
    raw = "|".join(sorted(tickers)) + f"|{period}|{interval}"
    return hashlib.md5(raw.encode()).hexdigest()


def read_cache(key: str, cache_dir: Path | str | None = None) -> pd.DataFrame | None:
    """從磁碟快取讀取 DataFrame。

    Parameters
    ----------
    key:
        快取鍵值（由 :func:`cache_key` 產生）。
    cache_dir:
        快取目錄，預設為 ``.cache``。

    Returns
    -------
    pd.DataFrame or None
        快取中的 DataFrame，若不存在則回傳 ``None``。
    """
    cache_dir = Path(cache_dir) if cache_dir else _DEFAULT_CACHE_DIR
    path = cache_dir / f"{key}.parquet"
    if path.exists():
        logger.info("從快取讀取: %s", path)
        return pd.read_parquet(path)
    return None


def write_cache(
    df: pd.DataFrame,
    key: str,
    cache_dir: Path | str | None = None,
) -> Path:
    """將 DataFrame 寫入磁碟快取。

    Parameters
    ----------
    df:
        要快取的 DataFrame。
    key:
        快取鍵值。
    cache_dir:
        快取目錄，預設為 ``.cache``。

    Returns
    -------
    Path
        快取檔案路徑。
    """
    cache_dir = Path(cache_dir) if cache_dir else _DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{key}.parquet"
    df.to_parquet(path, index=True)
    logger.info("已寫入快取: %s", path)
    return path
