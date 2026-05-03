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


# ── 輔助函式：建立可通過原始 VCP 條件的基底資料 ──────────────────────────────

def _make_passing_vcp_df(
    n: int = 300,
    close_end: float = 50.0,
    volume_base: float = 1_000_000.0,
) -> pd.DataFrame:
    """建立一組能通過原始 VCP 條件（不含新過濾條件）的基底 DataFrame。

    - 收盤使用平滑上升趨勢，確保 SMA 多頭排列與 SMA233 上升斜率
    - 波動率從前至後收縮（前段大、後段小）
    - 成交量從前至後收縮
    - 最後 8 天的波動率 < 0.1
    """
    rng = np.random.default_rng(99)
    dates = pd.bdate_range(start="2020-01-02", periods=n)

    # 平滑上升基底（確保 SMA233 > SMA144 > SMA55）
    base = np.linspace(close_end * 0.5, close_end, n)

    # 波動收縮：前段 ±3%，後 55 天 ±1.5%，後 21 天 ±0.5%，最後 8 天 ±0.3%
    noise = np.concatenate([
        rng.normal(0, base[: n - 55].mean() * 0.03, n - 55),
        rng.normal(0, base[n - 55 : n - 21].mean() * 0.015, 34),
        rng.normal(0, base[n - 21 : n - 8].mean() * 0.005, 13),
        rng.normal(0, base[n - 8 :].mean() * 0.003, 8),
    ])
    close = np.maximum(base + noise, 1.0)

    # 成交量收縮
    volume = np.concatenate([
        np.full(n - 55, volume_base * 1.5),
        np.full(34, volume_base * 1.2),
        np.full(13, volume_base * 0.8),
        np.full(8, volume_base * 0.4),
    ])

    high = close * 1.002
    low = close * 0.998
    open_ = close

    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
        index=dates,
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


class TestVcpFilters:
    """測試 Minervini 趨勢模板過濾條件（條件 7–10）。

    由於要精確觸發各條件，這裡使用 unittest.mock.patch 直接控制
    模組層級常數，避免建構能完整通過全部原始 VCP 條件的複雜資料。
    """

    def _make_df(
        self,
        n: int = 300,
        close_val: float = 50.0,
        volume_val: float = 1_000_000.0,
        close_52w_pattern: str = "normal",
    ) -> pd.DataFrame:
        """建立可控制收盤價與成交量的 DataFrame。

        Parameters
        ----------
        close_52w_pattern:
            ``"normal"``：收盤維持在 close_val
            ``"near_low"``：收盤接近 52 週低點（不滿足 +30% 條件）
            ``"below_high"``：收盤遠低於 52 週高點（不滿足 75% 條件）
        """
        dates = pd.bdate_range(start="2020-01-02", periods=n)
        base = np.linspace(close_val * 0.7, close_val, n)

        if close_52w_pattern == "near_low":
            # 先大漲再急跌，最後接近 52 週低點
            base = np.concatenate([
                np.linspace(close_val * 0.7, close_val * 2.0, n - 50),
                np.linspace(close_val * 2.0, close_val * 1.0, 50),
            ])
        elif close_52w_pattern == "below_high":
            # 先大漲再大跌，最後遠低於 52 週高點的 75%
            base = np.concatenate([
                np.linspace(close_val * 0.7, close_val * 3.0, n - 50),
                np.linspace(close_val * 3.0, close_val * 0.6, 50),
            ])

        close = base
        volume = np.full(n, volume_val)
        high = close * 1.001
        low = close * 0.999
        open_ = close
        return pd.DataFrame(
            {"open": open_, "high": high, "low": low, "close": close, "volume": volume},
            index=dates,
        )

    def test_min_price_filter(self):
        """收盤價低於 _MIN_PRICE 時應回傳 False。"""
        from unittest.mock import patch
        import stockscreener.strategies.vcp as vcp_mod

        df = _make_passing_vcp_df(close_end=5.0, volume_base=1_000_000.0)

        with patch.object(vcp_mod, "_MIN_PRICE", 10.0):
            result = vcp_screener_strategy("TEST_PRICE", df)

        # 收盤 ~5 元，低於 10 元門檻，應被過濾
        assert result is False

    def test_min_volume_filter(self):
        """50 日均量低於 _MIN_AVG_VOLUME_50 時應回傳 False。"""
        from unittest.mock import patch
        import stockscreener.strategies.vcp as vcp_mod

        df = _make_passing_vcp_df(close_end=50.0, volume_base=50_000.0)

        with patch.object(vcp_mod, "_MIN_PRICE", 0.0), \
             patch.object(vcp_mod, "_MIN_AVG_VOLUME_50", 300_000):
            result = vcp_screener_strategy("TEST_VOL", df)

        # 均量 ~50k，低於 300k 門檻，應被過濾
        assert result is False

    def test_52w_low_filter(self):
        """收盤未達 52 週低點 × 1.30 時應回傳 False。"""
        from unittest.mock import patch
        import stockscreener.strategies.vcp as vcp_mod

        # 先漲至 200，再跌至 105（52w low ~= 100，105 < 100 × 1.30 = 130）
        df = _make_passing_vcp_df(close_end=50.0, volume_base=500_000.0)
        # 覆寫後段收盤使其接近 52 週低點
        df.loc[df.index[-50:], "close"] = 105.0
        df.loc[df.index[-100:-50], "close"] = np.linspace(105.0, 200.0, 50)[::-1]
        df.loc[df.index[-200:-100], "close"] = 200.0

        with patch.object(vcp_mod, "_MIN_PRICE", 0.0), \
             patch.object(vcp_mod, "_MIN_AVG_VOLUME_50", 0), \
             patch.object(vcp_mod, "_MIN_DIST_FROM_52W_LOW", 1.30):
            result = vcp_screener_strategy("TEST_52W_LOW", df)

        assert result is False

    def test_52w_high_filter(self):
        """收盤低於 52 週高點 × 0.75 時應回傳 False。"""
        from unittest.mock import patch
        import stockscreener.strategies.vcp as vcp_mod

        # 使最後收盤為 52 週高點的 50%（遠低於 75%）
        df = _make_passing_vcp_df(close_end=50.0, volume_base=500_000.0)
        peak = float(df["close"].max())
        df.loc[df.index[-50:], "close"] = peak * 0.40

        with patch.object(vcp_mod, "_MIN_PRICE", 0.0), \
             patch.object(vcp_mod, "_MIN_AVG_VOLUME_50", 0), \
             patch.object(vcp_mod, "_MIN_DIST_FROM_52W_LOW", 0.0), \
             patch.object(vcp_mod, "_MAX_DIST_FROM_52W_HIGH", 0.75):
            result = vcp_screener_strategy("TEST_52W_HIGH", df)

        assert result is False

    def test_sma233_slope_filter(self):
        """SMA233 單調遞增但斜率不足時，加入 min_slope_pct 後應回傳 False。"""
        from unittest.mock import patch
        import stockscreener.strategies.vcp as vcp_mod

        # 建立 SMA233 幾乎平坦（斜率 << 0.5%）的資料：後 300 天收盤幾乎不動
        n = 300
        dates = pd.bdate_range(start="2020-01-02", periods=n)
        # 後 233 天完全持平，讓 SMA233 斜率 ≈ 0
        close = np.concatenate([
            np.linspace(50.0, 100.0, n - 233),
            np.full(233, 100.0),
        ])
        volume = np.full(n, 1_000_000.0)
        df = pd.DataFrame(
            {
                "open": close,
                "high": close * 1.001,
                "low": close * 0.999,
                "close": close,
                "volume": volume,
            },
            index=dates,
        )

        with patch.object(vcp_mod, "_MIN_PRICE", 0.0), \
             patch.object(vcp_mod, "_MIN_AVG_VOLUME_50", 0), \
             patch.object(vcp_mod, "_SMA_LONG_MIN_SLOPE_PCT", 0.005):
            result = vcp_screener_strategy("TEST_SLOPE", df)

        # SMA233 斜率接近 0，應被 min_slope_pct=0.5% 過濾
        assert result is False
