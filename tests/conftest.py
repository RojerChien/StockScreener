"""pytest 共用 fixtures - 所有測試使用 mock，不打真實外部 API。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def _make_ohlcv(n: int = 300, start: str = "2022-01-03", seed: int = 42) -> pd.DataFrame:
    """建立模擬 OHLCV DataFrame（欄位均小寫，DatetimeIndex）。"""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, periods=n)
    close = 100.0 + np.cumsum(rng.normal(0, 1, n))
    close = np.maximum(close, 1.0)
    high = close * (1 + rng.uniform(0, 0.02, n))
    low = close * (1 - rng.uniform(0, 0.02, n))
    open_ = close * (1 + rng.uniform(-0.01, 0.01, n))
    volume = rng.integers(500_000, 5_000_000, n).astype(float)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=dates,
    )


@pytest.fixture
def sample_ohlcv() -> pd.DataFrame:
    """300 個交易日的模擬 OHLCV 資料。"""
    return _make_ohlcv(300)


@pytest.fixture
def sample_ohlcv_short() -> pd.DataFrame:
    """50 個交易日的短期模擬資料（資料不足的邊界測試用）。"""
    return _make_ohlcv(50)


@pytest.fixture
def trending_up_ohlcv() -> pd.DataFrame:
    """持續上漲的模擬資料（用於 SMA crossover 觸發測試）。"""
    n = 400
    dates = pd.bdate_range(start="2020-01-02", periods=n)
    close = np.linspace(10, 200, n)
    high = close * 1.01
    low = close * 0.99
    open_ = close * 1.005
    volume = np.full(n, 1_000_000.0)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=dates,
    )


@pytest.fixture
def vcp_like_ohlcv() -> pd.DataFrame:
    """符合 VCP 條件的模擬資料：波動率收縮 + 成交量收縮 + SMA 多頭排列。"""
    n = 300
    rng = np.random.default_rng(0)
    dates = pd.bdate_range(start="2021-01-04", periods=n)

    # 建立上升趨勢的基底
    base = np.linspace(50, 100, n)

    # 前段（55~21 天前）波動較大
    noise = np.concatenate([
        rng.normal(0, 3, n - 55),   # 前段大波動
        rng.normal(0, 1.5, 34),     # 中段
        rng.normal(0, 0.5, 21),     # 後段小波動（VCP 收縮）
    ])
    close = np.maximum(base + noise, 1.0)

    # 成交量也收縮
    volume = np.concatenate([
        rng.integers(2_000_000, 4_000_000, n - 55),
        rng.integers(1_000_000, 2_000_000, 34),
        rng.integers(300_000, 800_000, 21),
    ]).astype(float)

    high = close * 1.005
    low = close * 0.995
    open_ = close * 1.001
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=dates,
    )
