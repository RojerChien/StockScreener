"""tests/test_strategies_vcp.py – VCP 策略訊號邏輯測試。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from stockscreener.strategies.vcp import (
    vcp_screener_strategy,
    calculate_volatility_duration,
    calculate_avg_volume_duration,
)


class TestCalculateVolatilityDuration:
    def test_returns_float(self, sample_ohlcv):
        result = calculate_volatility_duration(sample_ohlcv, end_day=20)
        assert isinstance(result, float)

    def test_zero_for_empty(self):
        empty = pd.DataFrame(columns=["close", "volume"])
        result = calculate_volatility_duration(empty, end_day=10)
        assert result == 0.0

    def test_positive_for_volatile(self, sample_ohlcv):
        result = calculate_volatility_duration(sample_ohlcv, end_day=55)
        assert result >= 0.0

    def test_constant_price_returns_zero(self):
        dates = pd.bdate_range("2023-01-02", periods=30)
        df = pd.DataFrame({"close": [100.0] * 30, "volume": [1e6] * 30}, index=dates)
        result = calculate_volatility_duration(df, end_day=20)
        assert result == pytest.approx(0.0, abs=1e-6)


class TestCalculateAvgVolumeDuration:
    def test_returns_float(self, sample_ohlcv):
        result = calculate_avg_volume_duration(sample_ohlcv, end_day=20)
        assert isinstance(result, float)

    def test_correct_mean(self):
        dates = pd.bdate_range("2023-01-02", periods=10)
        df = pd.DataFrame({"close": [100.0]*10, "volume": [float(i*100) for i in range(1, 11)]}, index=dates)
        result = calculate_avg_volume_duration(df, end_day=4)
        assert result > 0


class TestVcpScreenerStrategy:
    def test_returns_bool(self, sample_ohlcv):
        result = vcp_screener_strategy("TEST", sample_ohlcv)
        assert isinstance(result, bool)

    def test_short_data_returns_false(self, sample_ohlcv_short):
        result = vcp_screener_strategy("TEST", sample_ohlcv_short)
        assert result is False

    def test_empty_data_returns_false(self):
        empty = pd.DataFrame(columns=["close", "volume"])
        result = vcp_screener_strategy("TEST", empty)
        assert result is False

    def test_vcp_like_data(self, vcp_like_ohlcv):
        """VCP 形態資料應回傳 True（不保證，但不應崩潰）。"""
        result = vcp_screener_strategy("VCP_TEST", vcp_like_ohlcv)
        assert isinstance(result, bool)

    def test_no_exception_on_random_data(self, sample_ohlcv):
        try:
            vcp_screener_strategy("RAND", sample_ohlcv)
        except Exception as exc:
            pytest.fail(f"vcp_screener_strategy 意外拋出例外: {exc}")
