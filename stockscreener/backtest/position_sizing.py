"""stockscreener.backtest.position_sizing – position sizing functions.

Each sizing function must have the signature:
    fn(balance, buy_price, sell_price, state) -> (shares_to_buy, updated_state)

The ``state`` dict is passed between calls to carry investment tracking info
(e.g. pyramid stage reached).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

__all__ = ["pyramid_sizing", "fixed_sizing"]

# 金字塔加碼參數（對應 Backtest_pyramid_record.py）
_PYRAMID_RATIOS: List[float] = [0.1, 0.50, 1.0]
_PYRAMID_THRESHOLDS: List[float] = [0.0, 0.03, 0.06]


def pyramid_sizing(
    balance: float,
    buy_price: float,
    sell_price: float,
    state: Dict[str, Any],
    investment_ratios: List[float] | None = None,
    investment_thresholds: List[float] | None = None,
) -> Tuple[int, Dict[str, Any]]:
    """金字塔加碼倉位計算。

    加碼邏輯：
    - 第一筆：無論如何投入 10% 資金
    - 第二筆：若獲利 >= 3%，額外投入 50% 資金
    - 第三筆：若獲利 >= 6% 且第二筆已執行，額外投入 100% 資金

    此函式模擬整筆交易（使用最終賣價回推），與原始
    Backtest_pyramid_record.py 的計算方式一致。

    Parameters
    ----------
    balance:
        目前資金餘額。
    buy_price:
        買入價格。
    sell_price:
        賣出價格（最終平倉價）。
    state:
        用於在引擎呼叫間傳遞狀態的字典（此函式不使用）。
    investment_ratios:
        各階段投入比例，預設 ``[0.1, 0.50, 1.0]``。
    investment_thresholds:
        各階段觸發的最低獲利率，預設 ``[0.0, 0.03, 0.06]``。

    Returns
    -------
    tuple[int, dict]
        (shares_to_buy, state)
    """
    if investment_ratios is None:
        investment_ratios = _PYRAMID_RATIOS
    if investment_thresholds is None:
        investment_thresholds = _PYRAMID_THRESHOLDS

    current_profit_pct = (sell_price - buy_price) / buy_price if buy_price > 0 else 0.0

    total_shares = 0
    second_investment_made = False
    investment_made = False

    for idx, (ratio, threshold) in enumerate(zip(investment_ratios, investment_thresholds)):
        if current_profit_pct >= threshold:
            # 第三筆需在第二筆之後執行
            if idx == 2 and not second_investment_made:
                continue

            shares_to_buy = int(balance * ratio // buy_price)
            total_shares += shares_to_buy

            if idx == 1:
                second_investment_made = True
            investment_made = True

    # 若沒有任何投資觸發，至少投入第一筆（10%）
    if not investment_made:
        shares_to_buy = int(balance * investment_ratios[0] // buy_price)
        total_shares += shares_to_buy

    return total_shares, state


def fixed_sizing(
    balance: float,
    buy_price: float,
    sell_price: float,
    state: Dict[str, Any],
    ratio: float = 1.0,
) -> Tuple[int, Dict[str, Any]]:
    """固定比例倉位計算（使用全部餘額的指定比例）。

    Parameters
    ----------
    balance:
        目前資金餘額。
    buy_price:
        買入價格。
    sell_price:
        賣出價格（未使用，為保持介面一致）。
    state:
        傳遞狀態用字典（此函式不使用）。
    ratio:
        投入資金比例，預設 1.0（全倉）。

    Returns
    -------
    tuple[int, dict]
        (shares_to_buy, state)
    """
    shares_to_buy = int(balance * ratio // buy_price) if buy_price > 0 else 0
    return shares_to_buy, state
