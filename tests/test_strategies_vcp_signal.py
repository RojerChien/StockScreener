"""tests/test_strategies_vcp_signal.py – VCP 突破訊號函式測試。"""

from __future__ import annotations

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from stockscreener.strategies.vcp_signal import vcp_breakout_signals


# ── 輔助函式 ────────────────────────────────────────────────────────────────


def _make_df(
    n: int = 400,
    close: np.ndarray | None = None,
    volume: np.ndarray | None = None,
) -> pd.DataFrame:
    """建立含 DatetimeIndex 的 OHLCV DataFrame。"""
    dates = pd.bdate_range(start="2019-01-02", periods=n)
    if close is None:
        close = np.linspace(50.0, 120.0, n)
    if volume is None:
        volume = np.full(n, 1_000_000.0)
    return pd.DataFrame(
        {
            "open": close,
            "high": close * 1.005,
            "low": close * 0.995,
            "close": close,
            "volume": volume,
        },
        index=dates,
    )


def _all_false_mask(df: pd.DataFrame) -> pd.Series:
    return pd.Series(False, index=df.index)


def _all_true_mask(df: pd.DataFrame) -> pd.Series:
    return pd.Series(True, index=df.index)


def _mask_true_at(df: pd.DataFrame, idx: int) -> pd.Series:
    """只在指定 integer 位置為 True 的遮罩。"""
    mask = pd.Series(False, index=df.index)
    mask.iloc[idx] = True
    return mask


# ── 測試類別 ────────────────────────────────────────────────────────────────


class TestVcpBreakoutSignals:
    def test_returns_paired_lists(self):
        """buy / sell 訊號應等長，且都是列表型別。"""
        df = _make_df()

        with patch(
            "stockscreener.strategies.vcp_signal._precompute_vcp_mask",
            return_value=_all_false_mask(df),
        ):
            buy, sell = vcp_breakout_signals(df)

        assert isinstance(buy, list)
        assert isinstance(sell, list)
        assert len(buy) == len(sell)

    def test_no_trade_without_vcp(self):
        """VCP 遮罩全為 False 時，不應產生任何訊號。"""
        df = _make_df()

        with patch(
            "stockscreener.strategies.vcp_signal._precompute_vcp_mask",
            return_value=_all_false_mask(df),
        ):
            buy, sell = vcp_breakout_signals(df)

        assert len(buy) == 0
        assert len(sell) == 0

    def test_no_trade_without_breakout(self):
        """VCP 通過但收盤未突破前高（平盤）時，不應產生進場訊號。"""
        close = np.full(400, 100.0)
        df = _make_df(close=close)

        with patch(
            "stockscreener.strategies.vcp_signal._precompute_vcp_mask",
            return_value=_all_true_mask(df),
        ):
            buy, sell = vcp_breakout_signals(df)

        # 平盤：close_cur == prev_high，不滿足嚴格突破條件
        assert len(buy) == 0

    def test_stop_loss_triggers(self):
        """進場後下跌超過停損比例，應在當日產生賣出訊號。"""
        n = 400
        entry_idx = 300
        entry_price = 121.0

        close = np.concatenate([
            np.linspace(50.0, 119.5, entry_idx),  # 前段上升（最高 ~119.5）
            [entry_price],                          # 突破進場（高於前高）
            np.full(n - entry_idx - 1, 100.0),     # 急跌 > 7% → 觸發停損
        ])
        volume = np.full(n, 1_000_000.0)
        volume[entry_idx] = 2_000_000.0
        df = _make_df(n=n, close=close, volume=volume)

        # VCP 在 entry_idx-1 觸發 → vcp_prev 在 entry_idx 為 True
        mask = _mask_true_at(df, entry_idx - 1)

        with patch(
            "stockscreener.strategies.vcp_signal._precompute_vcp_mask",
            return_value=mask,
        ):
            buy, sell = vcp_breakout_signals(
                df,
                stop_loss_pct=0.07,
                profit_target_pct=0.99,   # 停用獲利了結
                volume_multiplier=1.0,
            )

        assert len(buy) == len(sell)
        assert len(buy) > 0, "應有進場訊號"
        sell_price = float(df.loc[sell[0], "close"])
        # 100.0 < 121.0 * 0.93 = 112.53，停損應觸發
        assert sell_price <= entry_price * (1 - 0.05)

    def test_profit_target_triggers(self):
        """進場後上漲超過獲利目標比例，應在當日產生賣出訊號。"""
        n = 400
        entry_idx = 300
        entry_price = 121.0
        target_price = entry_price * 1.25  # 151.25

        close = np.concatenate([
            np.linspace(50.0, 119.5, entry_idx),
            [entry_price],                         # 進場
            np.full(n - entry_idx - 1, 160.0),    # 大漲 > 25%
        ])
        volume = np.full(n, 1_000_000.0)
        volume[entry_idx] = 2_000_000.0
        df = _make_df(n=n, close=close, volume=volume)

        mask = _mask_true_at(df, entry_idx - 1)

        with patch(
            "stockscreener.strategies.vcp_signal._precompute_vcp_mask",
            return_value=mask,
        ):
            buy, sell = vcp_breakout_signals(
                df,
                stop_loss_pct=0.99,       # 停用停損
                profit_target_pct=0.25,
                volume_multiplier=1.0,
            )

        assert len(buy) == len(sell)
        assert len(buy) > 0, "應有進場訊號"
        sell_price = float(df.loc[sell[0], "close"])
        assert sell_price >= target_price

    def test_empty_data_returns_empty(self):
        """空 DataFrame 應回傳兩個空列表，且不崩潰。"""
        empty = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        buy, sell = vcp_breakout_signals(empty)
        assert buy == []
        assert sell == []

    def test_short_data_returns_empty(self):
        """資料長度不足 233 天應直接回傳空列表。"""
        df = _make_df(n=200)
        buy, sell = vcp_breakout_signals(df)
        assert buy == []
        assert sell == []
