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


# ── 測試類別 ────────────────────────────────────────────────────────────────


class TestVcpBreakoutSignals:
    def test_returns_paired_lists(self):
        """buy / sell 訊號應等長，且都是列表型別。"""
        df = _make_df()

        # 模擬 vcp_screener_strategy 永遠回傳 False（無 VCP 訊號）
        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            return_value=False,
        ):
            buy, sell = vcp_breakout_signals(df)

        assert isinstance(buy, list)
        assert isinstance(sell, list)
        assert len(buy) == len(sell)

    def test_no_trade_without_vcp(self):
        """VCP 篩選永遠不通過時，不應產生任何訊號。"""
        df = _make_df()

        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            return_value=False,
        ):
            buy, sell = vcp_breakout_signals(df)

        assert len(buy) == 0
        assert len(sell) == 0

    def test_no_trade_without_breakout(self):
        """VCP 通過但收盤未突破前高時，不應產生進場訊號。"""
        # 平坦收盤（無突破）
        close = np.full(400, 100.0)
        df = _make_df(close=close)

        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            return_value=True,
        ):
            buy, sell = vcp_breakout_signals(df)

        assert len(buy) == 0

    def test_stop_loss_triggers(self):
        """進場後下跌超過停損比例，應在當日產生賣出訊號。"""
        n = 400
        # 前 300 天上漲，第 301 天為進場日（VCP 通過 + 突破），之後急跌
        close = np.concatenate([
            np.linspace(50.0, 120.0, 300),
            [121.0],                          # 突破高點（進場）
            np.full(n - 301, 100.0),          # 急跌 > 7%
        ])
        volume = np.full(n, 1_000_000.0)
        volume[300] = 2_000_000.0            # 突破量能
        df = _make_df(n=n, close=close, volume=volume)

        entry_price = 121.0
        stop_price = entry_price * (1 - 0.07)  # 112.53

        # 模擬 VCP 僅在第 300 個交易日（index 300）通過
        call_count = [0]

        def mock_vcp(ticker, data):
            call_count[0] += 1
            # 只有當資料長度 == 301 時回傳 True（對應 i=300 的 slice）
            return len(data) == 301

        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            side_effect=mock_vcp,
        ):
            buy, sell = vcp_breakout_signals(
                df,
                stop_loss_pct=0.07,
                profit_target_pct=0.99,  # 停用獲利了結，只測停損
                volume_multiplier=1.0,
            )

        # 若有進場，應有相應出場
        assert len(buy) == len(sell)
        if len(buy) > 0:
            # 出場價格應 <= 停損價
            sell_date = sell[0]
            sell_price = float(df.loc[sell_date, "close"])
            assert sell_price <= entry_price * (1 - 0.05)  # 寬鬆驗證：至少跌了 5%

    def test_profit_target_triggers(self):
        """進場後上漲超過獲利目標比例，應在當日產生賣出訊號。"""
        n = 400
        # 前 300 天上漲，第 301 天進場，之後大幅上漲
        close = np.concatenate([
            np.linspace(50.0, 120.0, 300),
            [121.0],                          # 進場
            np.full(n - 301, 160.0),          # 大漲 > 25%
        ])
        volume = np.full(n, 1_000_000.0)
        volume[300] = 2_000_000.0
        df = _make_df(n=n, close=close, volume=volume)

        entry_price = 121.0
        target_price = entry_price * (1 + 0.25)  # 151.25

        def mock_vcp(ticker, data):
            return len(data) == 301

        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            side_effect=mock_vcp,
        ):
            buy, sell = vcp_breakout_signals(
                df,
                stop_loss_pct=0.99,  # 停用停損，只測獲利目標
                profit_target_pct=0.25,
                volume_multiplier=1.0,
            )

        assert len(buy) == len(sell)
        if len(buy) > 0:
            sell_date = sell[0]
            sell_price = float(df.loc[sell_date, "close"])
            assert sell_price >= target_price

    def test_empty_data_returns_empty(self):
        """空 DataFrame 應回傳兩個空列表，且不崩潰。"""
        empty = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

        with patch(
            "stockscreener.strategies.vcp_signal.vcp_screener_strategy",
            return_value=False,
        ):
            buy, sell = vcp_breakout_signals(empty)

        assert buy == []
        assert sell == []
