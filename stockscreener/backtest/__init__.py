"""stockscreener.backtest – backtesting sub-package."""

from __future__ import annotations

from .engine import BacktestEngine, BacktestResult
from .position_sizing import pyramid_sizing, fixed_sizing
from .report import generate_html_report

__all__ = [
    "BacktestEngine",
    "BacktestResult",
    "pyramid_sizing",
    "fixed_sizing",
    "generate_html_report",
]
