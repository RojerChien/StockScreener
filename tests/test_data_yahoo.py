"""tests/test_data_yahoo.py – Yahoo 資料擷取與欄位正規化測試。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from stockscreener.data.yahoo import normalize_columns, sel_yq_historical_data


class TestNormalizeColumns:
    def test_capitalised_to_lower(self):
        df = pd.DataFrame({"Close": [1.0], "Volume": [100], "Open": [1.0],
                           "High": [1.1], "Low": [0.9]})
        result = normalize_columns(df)
        assert "close" in result.columns
        assert "volume" in result.columns
        assert "Close" not in result.columns

    def test_already_lower_unchanged(self):
        df = pd.DataFrame({"close": [1.0], "volume": [100]})
        result = normalize_columns(df)
        assert list(result.columns) == ["close", "volume"]

    def test_unknown_columns_unchanged(self):
        """normalize_columns 只映射已知大寫欄位，不處理任意命名。"""
        df = pd.DataFrame({"CLOSE": [1.0], "Volume": [100]})
        result = normalize_columns(df)
        # Volume 被轉換，CLOSE 不在映射表中故不轉換
        assert "volume" in result.columns
        assert "CLOSE" in result.columns  # 未映射的欄位保持原樣

    def test_adj_close_mapped(self):
        df = pd.DataFrame({"Adj Close": [1.0]})
        result = normalize_columns(df)
        assert "adj_close" in result.columns


class TestSelYqHistoricalData:
    def _make_multiindex_df(self):
        dates = pd.bdate_range("2023-01-02", periods=5)
        tickers = ["AAPL", "TSLA"]
        idx = pd.MultiIndex.from_product([tickers, dates], names=["symbol", "date"])
        data = {
            "close": np.random.rand(10) * 100 + 50,
            "volume": np.random.randint(1_000_000, 5_000_000, 10).astype(float),
        }
        return pd.DataFrame(data, index=idx)

    def test_returns_correct_ticker(self):
        df_all = self._make_multiindex_df()
        result = sel_yq_historical_data(df_all, "AAPL")
        assert not result.empty
        assert len(result) == 5

    def test_missing_ticker_returns_empty(self):
        df_all = self._make_multiindex_df()
        result = sel_yq_historical_data(df_all, "NVDA")
        assert result.empty

    def test_returns_copy(self):
        df_all = self._make_multiindex_df()
        result = sel_yq_historical_data(df_all, "AAPL")
        result["close"] = 999.0  # modify copy
        original = sel_yq_historical_data(df_all, "AAPL")
        assert not (original["close"] == 999.0).all()
