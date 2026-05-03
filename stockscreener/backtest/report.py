"""stockscreener.backtest.report – HTML report generator for backtest results."""

from __future__ import annotations

import logging
import webbrowser
from pathlib import Path
from typing import List, Optional

import pandas as pd

from .engine import BacktestResult

logger = logging.getLogger(__name__)

__all__ = ["generate_html_report"]

_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="stylesheet" type="text/css"
        href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
  <script>
    $(document).ready(function() {{
      $('#resultsTable').DataTable({{
        "pageLength": -1,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
      }});
    }});
  </script>
</head>
<body>
<h2>{title}</h2>
{table}
</body>
</html>
"""


def generate_html_report(
    results: List[BacktestResult],
    output_path: str | Path = "backtest_results.html",
    title: str = "Backtest Results",
    open_browser: bool = True,
) -> Path:
    """將回測結果列表轉換為 HTML 報表並儲存。

    Parameters
    ----------
    results:
        :class:`BacktestResult` 物件列表。
    output_path:
        輸出 HTML 檔案路徑，預設 ``backtest_results.html``。
    title:
        報表標題。
    open_browser:
        是否自動以瀏覽器開啟報表，預設 ``True``。

    Returns
    -------
    Path
        已儲存的 HTML 檔案路徑。
    """
    rows = [
        {
            "Ticker": r.ticker,
            "Total Trades": r.total_trades,
            "Winning %": round(r.winning_percentage, 2),
            "Initial Balance": round(r.initial_balance, 2),
            "Final Balance": round(r.final_balance, 2),
            "Total Return %": round(r.total_return, 2),
        }
        for r in results
    ]

    df = pd.DataFrame(rows)
    table_html = df.to_html(index=False, classes="sortable", table_id="resultsTable")
    final_html = _HTML_TEMPLATE.format(title=title, table=table_html)

    output_path = Path(output_path)
    output_path.write_text(final_html, encoding="utf-8")
    logger.info("回測報表已儲存: %s", output_path)

    if open_browser:
        webbrowser.open(str(output_path))

    return output_path
