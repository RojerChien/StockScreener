"""stockscreener.backtest.engine – generic event-driven backtest engine.

Strategy Pattern: accepts a *signal_fn* (produces buy/sell dates) and a
*sizing_fn* (determines how many shares to buy at each investment step).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["BacktestEngine", "BacktestResult"]

# 預設初始資金（對應 Backtest_pyramid_record.py）
_DEFAULT_INITIAL_BALANCE = 200_000.0

# 型別別名
SignalFn = Callable[[pd.DataFrame], Tuple[List, List]]
SizingFn = Callable[[float, float, float, Dict[str, Any]], Tuple[int, Dict[str, Any]]]


@dataclass
class BacktestResult:
    """單次回測結果的資料容器。"""

    ticker: str
    winning_percentage: float
    initial_balance: float
    final_balance: float
    total_return: float
    total_trades: int
    trade_records: List[Dict[str, Any]] = field(default_factory=list)


class BacktestEngine:
    """事件驅動回測引擎。

    Parameters
    ----------
    signal_fn:
        接收 DataFrame，回傳 ``(buy_signals, sell_signals)`` 的函式。
    sizing_fn:
        接收 ``(balance, buy_price, sell_price, state)`` 並回傳
        ``(shares_to_buy, updated_state)`` 的函式。
        ``state`` 字典可用於在多次投資步驟間傳遞狀態。
    initial_balance:
        初始資金，預設 200,000。
    """

    def __init__(
        self,
        signal_fn: SignalFn,
        sizing_fn: SizingFn,
        initial_balance: float = _DEFAULT_INITIAL_BALANCE,
    ) -> None:
        self.signal_fn = signal_fn
        self.sizing_fn = sizing_fn
        self.initial_balance = initial_balance

    def run(self, data: pd.DataFrame, ticker: str = "UNKNOWN") -> BacktestResult:
        """執行回測。

        Parameters
        ----------
        data:
            含有 ``close`` 欄位的 DataFrame（DatetimeIndex）。
        ticker:
            股票代號，用於記錄 log 與結果標記。

        Returns
        -------
        BacktestResult
        """
        buy_signals, sell_signals = self.signal_fn(data)

        if len(buy_signals) != len(sell_signals):
            # 保持配對
            min_len = min(len(buy_signals), len(sell_signals))
            buy_signals = buy_signals[:min_len]
            sell_signals = sell_signals[:min_len]

        balance = self.initial_balance
        shares = 0
        profit_count = 0
        total_trades = len(buy_signals)
        trade_records: List[Dict[str, Any]] = []

        for buy_date, sell_date in zip(buy_signals, sell_signals):
            buy_price = float(data.loc[buy_date, "close"])
            sell_price = float(data.loc[sell_date, "close"])

            state: Dict[str, Any] = {}
            total_shares = 0
            total_investment = 0.0
            investment_count = 0

            # 讓 sizing_fn 決定本次交易買多少股
            shares_bought, state = self.sizing_fn(balance, buy_price, sell_price, state)
            if shares_bought > 0:
                total_shares += shares_bought
                cost = shares_bought * buy_price
                balance -= cost
                total_investment += cost
                investment_count += 1

            # 平倉
            proceeds = total_shares * sell_price
            balance += proceeds
            profit = total_shares * (sell_price - buy_price)
            if profit > 0:
                profit_count += 1
            total_shares = 0

            record: Dict[str, Any] = {
                "buy_date": buy_date,
                "buy_price": buy_price,
                "sell_date": sell_date,
                "sell_price": sell_price,
                "exposure_days": sell_date - buy_date,
                "investment_amount": total_investment,
                "investment_count": investment_count,
                "profit": profit,
                "balance": balance,
                "cumulative_profit": balance - self.initial_balance,
            }
            trade_records.append(record)

        winning_percentage = (profit_count / total_trades * 100) if total_trades > 0 else 0.0
        final_balance = balance + shares * float(data["close"].iloc[-1])
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100

        logger.info(
            "%s 回測結果: 勝率 %.1f%%, 總報酬 %.2f%%",
            ticker,
            winning_percentage,
            total_return,
        )

        return BacktestResult(
            ticker=ticker,
            winning_percentage=winning_percentage,
            initial_balance=self.initial_balance,
            final_balance=final_balance,
            total_return=total_return,
            total_trades=total_trades,
            trade_records=trade_records,
        )
