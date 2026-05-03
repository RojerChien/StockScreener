"""stockscreener.charts.highstock – OHLCV + VWAP + RSI chart renderer (Plotly).

Chart layout:
  - OHLC candlestick  (70% height), red down / green up
  - Volume column     (15% height), red if open > close else green
  - RSI line          (15% height), dashed lines at 30 and 70
  - VWAP lines: 5 (blue), 21 (orange), 55 (red), 144 (purple)
  - Show/Hide VWAP buttons
  - TradingView link in title
Output: save as {ticker}_{date}.html and webbrowser.open()

Note: Uses Plotly for reliable rendering without CDN dependencies.
"""

from __future__ import annotations

import datetime
import logging
import webbrowser
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["render_highstock_chart"]

_TODAY = str(datetime.datetime.now().date())

_VWAP_COLORS = {5: "blue", 21: "orange", 55: "red", 144: "purple"}
_VWAP_LINE_WIDTH = 2


def render_highstock_chart(
    df: pd.DataFrame,
    ticker: str,
    tradingview_url: str = "",
    date: str = _TODAY,
    output_dir: str | Path = ".",
    open_browser: bool = True,
) -> Path:
    """產生 OHLCV + VWAP + RSI 互動式 HTML 圖表（Plotly）。

    DataFrame 必須包含欄位：``open``, ``high``, ``low``, ``close``,
    ``volume``, ``RSI``（可選），以及 ``vwap5``, ``vwap21``, ``vwap55``,
    ``vwap144``（可選）。

    Parameters
    ----------
    df:
        單一股票的歷史資料 DataFrame（DatetimeIndex）。
    ticker:
        股票代號（用於圖表標題與檔名）。
    tradingview_url:
        TradingView 連結 URL（顯示於標題）。
    date:
        圖表日期字串，預設今日。
    output_dir:
        HTML 輸出目錄，預設當前目錄。
    open_browser:
        是否自動以瀏覽器開啟，預設 ``True``。

    Returns
    -------
    Path
        已儲存的 HTML 檔案路徑。
    """
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        logger.error("plotly 未安裝，請執行 pip install plotly")
        raise

    df = df.copy()

    # 建立 3 列子圖：OHLC / 成交量 / RSI
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.70, 0.15, 0.15],
    )

    # ── 蠟燭圖（第 1 列）────────────────────────────────────────────────────
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name=ticker,
            increasing_line_color="green",
            decreasing_line_color="red",
        ),
        row=1,
        col=1,
    )

    # ── VWAP 線條（第 1 列）─────────────────────────────────────────────────
    vwap_trace_indices: list[int] = []
    for window, color in [(144, "purple"), (55, "red"), (21, "orange"), (5, "blue")]:
        col_name = f"vwap{window}"
        if col_name not in df.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col_name],
                name=f"VWAP{window}",
                line=dict(color=color, width=_VWAP_LINE_WIDTH),
                mode="lines",
            ),
            row=1,
            col=1,
        )
        vwap_trace_indices.append(len(fig.data) - 1)

    # ── 成交量柱狀圖（第 2 列）──────────────────────────────────────────────
    bar_colors = [
        "red" if float(o) > float(c) else "green"
        for o, c in zip(df["open"], df["close"])
    ]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["volume"],
            name="成交量",
            marker_color=bar_colors,
            showlegend=True,
        ),
        row=2,
        col=1,
    )

    # ── 成交量 10 日移動平均（第 2 列）──────────────────────────────────────
    vol_ma = df["volume"].rolling(10).mean()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=vol_ma,
            name="10日量均",
            line=dict(color="orange", width=1.5),
            mode="lines",
        ),
        row=2,
        col=1,
    )

    # ── RSI（第 3 列）───────────────────────────────────────────────────────
    if "RSI" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["RSI"],
                name="RSI",
                line=dict(color="blue", width=1.5),
                mode="lines",
            ),
            row=3,
            col=1,
        )
        fig.add_hline(
            y=30, line=dict(color="red", width=1, dash="dot"), row=3, col=1
        )
        fig.add_hline(
            y=70, line=dict(color="red", width=1, dash="dot"), row=3, col=1
        )

    # ── VWAP 顯示/隱藏按鈕──────────────────────────────────────────────────
    n_total = len(fig.data)
    visible_all = [True] * n_total
    visible_no_vwap = [
        False if i in vwap_trace_indices else True for i in range(n_total)
    ]

    # ── 標題（含 TradingView 連結）──────────────────────────────────────────
    if tradingview_url:
        title_text = f'<a href="{tradingview_url}">{ticker}</a> ({date})'
    else:
        title_text = f"{ticker} ({date})"

    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor="center"),
        height=930,
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        xaxis3_rangeslider_visible=True,
        hovermode="x unified",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.0,
                y=1.08,
                xanchor="left",
                yanchor="top",
                buttons=[
                    dict(
                        label="Show VWAP",
                        method="restyle",
                        args=[{"visible": visible_all}],
                    ),
                    dict(
                        label="Hide VWAP",
                        method="restyle",
                        args=[{"visible": visible_no_vwap}],
                    ),
                ],
            )
        ],
    )

    fig.update_yaxes(title_text="OHLC", row=1, col=1, fixedrange=False)
    fig.update_yaxes(title_text="Volume", row=2, col=1, fixedrange=False)
    fig.update_yaxes(
        title_text="RSI", row=3, col=1, range=[0, 100], fixedrange=False
    )

    # ── 儲存並開啟──────────────────────────────────────────────────────────
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"{ticker}_{date}.html"

    fig.write_html(
        str(filename),
        include_plotlyjs=True,  # 嵌入 Plotly.js，不需要網路連線
    )

    logger.info("圖表已儲存: %s", filename)

    if open_browser:
        webbrowser.open(str(filename))

    return filename
