"""tests/test_indicators_zigzag.py – Zigzag 高低點偵測測試。"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from stockscreener.indicators.zigzag import calculate_zigzag


class TestDetectZigzag:
    def _make_wave(self) -> pd.DataFrame:
        """建立明顯波峰/波谷的正弦波資料。"""
        n = 200
        dates = pd.bdate_range("2022-01-03", periods=n)
        t = np.linspace(0, 4 * np.pi, n)
        close = 100 + 20 * np.sin(t)
        high = close + 1
        low = close - 1
        volume = np.full(n, 1_000_000.0)
        return pd.DataFrame(
            {"open": close, "high": high, "low": low, "close": close, "volume": volume},
            index=dates,
        )

    def test_returns_dataframe(self, sample_ohlcv):
        result = calculate_zigzag(sample_ohlcv)
        assert isinstance(result, pd.DataFrame)

    def test_has_price_column(self, sample_ohlcv):
        result = calculate_zigzag(sample_ohlcv)
        assert "price" in result.columns

    def test_alternating_peaks_valleys(self):
        """zigzag 點應交替出現高低點（相鄰點方向相反）。"""
        df = self._make_wave()
        result = calculate_zigzag(df, min_percentage=0.05)
        if len(result) < 3:
            pytest.skip("資料不足以偵測足夠的 zigzag 點")
        prices = result["price"].values
        # 相鄰兩點應方向相反
        for i in range(1, len(prices) - 1):
            prev_up = prices[i] > prices[i - 1]
            next_up = prices[i + 1] > prices[i]
            assert prev_up != next_up, f"index {i}: 方向未交替"

    def test_empty_dataframe_returns_empty(self):
        empty = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        result = calculate_zigzag(empty)
        assert result.empty

    def test_short_data_no_crash(self, sample_ohlcv_short):
        result = calculate_zigzag(sample_ohlcv_short)
        assert isinstance(result, pd.DataFrame)
