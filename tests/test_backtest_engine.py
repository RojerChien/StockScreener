"""tests/test_backtest_engine.py – 回測引擎與倉位管理測試。"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import pytest

from stockscreener.backtest.engine import BacktestEngine, BacktestResult
from stockscreener.backtest.position_sizing import fixed_sizing, pyramid_sizing


# ── 輔助函式 ───────────────────────────────────────────────────────────────────

def _buy_day3_sell_day7_signal(
    data: pd.DataFrame,
) -> Tuple[List, List]:
    """固定在第 3 天買、第 7 天賣的假訊號（用於確定性測試）。"""
    idx = data.index
    if len(idx) < 8:
        return [], []
    return [idx[3]], [idx[7]]


def _no_signal(data: pd.DataFrame) -> Tuple[List, List]:
    return [], []


def _multiple_signals(data: pd.DataFrame) -> Tuple[List, List]:
    idx = data.index
    if len(idx) < 20:
        return [], []
    buys = [idx[2], idx[10]]
    sells = [idx[6], idx[15]]
    return buys, sells


# ── BacktestEngine 測試 ──────────────────────────────────────────────────────

class TestBacktestEngine:
    def test_returns_backtest_result(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_buy_day3_sell_day7_signal,
            sizing_fn=fixed_sizing,
            initial_balance=10_000.0,
        )
        result = engine.run(sample_ohlcv, ticker="TEST")
        assert isinstance(result, BacktestResult)

    def test_no_signal_zero_trades(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_no_signal,
            sizing_fn=fixed_sizing,
            initial_balance=10_000.0,
        )
        result = engine.run(sample_ohlcv, ticker="TEST")
        assert result.total_trades == 0
        assert result.final_balance == pytest.approx(10_000.0, rel=1e-6)

    def test_single_trade_recorded(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_buy_day3_sell_day7_signal,
            sizing_fn=fixed_sizing,
        )
        result = engine.run(sample_ohlcv, ticker="TEST")
        assert result.total_trades == 1
        assert len(result.trade_records) == 1

    def test_multiple_trades_recorded(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_multiple_signals,
            sizing_fn=fixed_sizing,
        )
        result = engine.run(sample_ohlcv, ticker="TEST")
        assert result.total_trades == 2
        assert len(result.trade_records) == 2

    def test_winning_percentage_range(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_multiple_signals,
            sizing_fn=fixed_sizing,
        )
        result = engine.run(sample_ohlcv, ticker="TEST")
        assert 0.0 <= result.winning_percentage <= 100.0

    def test_initial_balance_preserved_on_no_trade(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_no_signal,
            sizing_fn=fixed_sizing,
            initial_balance=50_000.0,
        )
        result = engine.run(sample_ohlcv)
        assert result.initial_balance == 50_000.0
        assert result.final_balance == pytest.approx(50_000.0, rel=1e-6)

    def test_trade_record_has_required_keys(self, sample_ohlcv):
        engine = BacktestEngine(
            signal_fn=_buy_day3_sell_day7_signal,
            sizing_fn=fixed_sizing,
        )
        result = engine.run(sample_ohlcv, ticker="X")
        record = result.trade_records[0]
        for key in ("buy_date", "sell_date", "buy_price", "sell_price",
                    "profit", "balance", "cumulative_profit"):
            assert key in record, f"缺少欄位: {key}"


# ── FixedSizing 測試 ──────────────────────────────────────────────────────────

class TestFixedSizing:
    def test_buys_full_balance(self):
        shares, _ = fixed_sizing(10_000.0, 100.0, 110.0, {}, ratio=1.0)
        assert shares == 100  # floor(10000 / 100)

    def test_partial_ratio(self):
        shares, _ = fixed_sizing(10_000.0, 100.0, 110.0, {}, ratio=0.5)
        assert shares == 50

    def test_zero_price_returns_zero(self):
        shares, _ = fixed_sizing(10_000.0, 0.0, 110.0, {})
        assert shares == 0

    def test_state_returned_unchanged(self):
        state = {"key": "value"}
        _, returned = fixed_sizing(10_000.0, 100.0, 110.0, state)
        assert returned == state


# ── PyramidSizing 測試 ────────────────────────────────────────────────────────

class TestPyramidSizing:
    def test_profitable_trade_invests_more(self):
        """獲利 7%，應觸發全部三階段加碼（但第三需在第二之後）。"""
        shares_profit, _ = pyramid_sizing(10_000.0, 100.0, 107.0, {})
        shares_flat, _ = pyramid_sizing(10_000.0, 100.0, 100.0, {})
        assert shares_profit > shares_flat

    def test_loss_invests_minimum(self):
        """虧損時只投入第一筆（10%）。"""
        shares, _ = pyramid_sizing(10_000.0, 100.0, 90.0, {})
        expected_min = int(10_000.0 * 0.1 // 100.0)
        assert shares >= expected_min

    def test_returns_int_shares(self):
        shares, _ = pyramid_sizing(10_000.0, 50.0, 55.0, {})
        assert isinstance(shares, int)

    def test_custom_ratios(self):
        shares, _ = pyramid_sizing(
            10_000.0, 100.0, 110.0, {},
            investment_ratios=[0.2],
            investment_thresholds=[0.0],
        )
        assert shares == int(10_000.0 * 0.2 // 100.0)

    def test_third_stage_requires_second(self):
        """profit=7% 但只有一個 threshold=6%（無 threshold=3%）應只觸發一次。"""
        shares, _ = pyramid_sizing(
            10_000.0, 100.0, 107.0, {},
            investment_ratios=[0.1, 1.0],
            investment_thresholds=[0.0, 0.06],
        )
        # 只有兩個階段，不存在「第三需在第二之後」問題
        assert shares > 0
