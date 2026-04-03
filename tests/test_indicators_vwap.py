"""tests/test_indicators_vwap.py – VWAP 計算正確性測試。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from stockscreener.indicators.vwap import calculate_vwap, add_all_vwaps


class TestCalculateVwap:
    def test_column_added(self, sample_ohlcv):
        result = calculate_vwap(sample_ohlcv, window=21)
        assert "vwap21" in result.columns

    def test_first_rows_are_nan(self, sample_ohlcv):
        result = calculate_vwap(sample_ohlcv, window=21)
        # 前 20 列應為 NaN（rolling window 不足）
        assert result["vwap21"].iloc[:20].isna().all()

    def test_value_calculation(self):
        """用已知數值手動驗算 VWAP3。"""
        df = pd.DataFrame({
            "close":  [10.0, 11.0, 12.0, 13.0],
            "volume": [100.0, 200.0, 300.0, 400.0],
        }, index=pd.bdate_range("2023-01-02", periods=4))

        result = calculate_vwap(df, window=3)
        # vwap3 第 3 列（index=2）= sum(close*vol, 0:3) / sum(vol, 0:3)
        expected = (10*100 + 11*200 + 12*300) / (100 + 200 + 300)
        assert abs(result["vwap3"].iloc[2] - expected) < 1e-9

    def test_does_not_modify_original(self, sample_ohlcv):
        original_cols = list(sample_ohlcv.columns)
        calculate_vwap(sample_ohlcv, window=5)
        assert list(sample_ohlcv.columns) == original_cols

    def test_vwap_between_low_and_high(self, sample_ohlcv):
        result = calculate_vwap(sample_ohlcv, window=21)
        valid = result.dropna(subset=["vwap21"])
        assert (valid["vwap21"] > 0).all()


class TestAddAllVwaps:
    def test_adds_all_specified_windows(self, sample_ohlcv):
        windows = [5, 21, 55]
        result = add_all_vwaps(sample_ohlcv, windows=windows)
        for w in windows:
            assert f"vwap{w}" in result.columns

    def test_default_windows_added(self, sample_ohlcv):
        result = add_all_vwaps(sample_ohlcv)
        # 至少應有 vwap5 和 vwap21
        assert "vwap5" in result.columns
        assert "vwap21" in result.columns

    def test_vwprice_column_added(self, sample_ohlcv):
        result = add_all_vwaps(sample_ohlcv, windows=[21])
        assert "VWPrice" in result.columns
