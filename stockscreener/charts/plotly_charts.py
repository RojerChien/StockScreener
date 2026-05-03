"""stockscreener.charts.plotly_charts – Plotly OHLCV candlestick chart renderer."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["render_plotly_chart"]


def render_plotly_chart(
    df: pd.DataFrame,
    ticker: str,
    output_path: Optional[str | Path] = None,
    open_browser: bool = True,
    show_vwap: bool = True,
    show_rsi: bool = True,
) -> Optional[Path]:
    """產生 Plotly 互動式 OHLCV 圖表（含 VWAP 與 RSI）。

    Parameters
    ----------
    df:
        含有 ``open``, ``high``, ``low``, ``close``, ``volume`` 欄位的 DataFrame。
    ticker:
        股票代號（用於圖表標題）。
    output_path:
        HTML 輸出路徑；若為 ``None`` 則僅以瀏覽器開啟（不儲存）。
    open_browser:
        是否自動以瀏覽器開啟，預設 ``True``。
    show_vwap:
        是否疊加 VWAP 線，預設 ``True``。
    show_rsi:
        是否顯示 RSI 子圖，預設 ``True``。

    Returns
    -------
    Path or None
        HTML 檔案路徑（若有儲存），否則 ``None``。
    """
    try:
        import plotly.graph_objects as go  # type: ignore
        from plotly.subplots import make_subplots  # type: ignore
    except ImportError:
        logger.error("plotly 未安裝，無法產生 Plotly 圖表")
        raise

    rows = 2 if show_rsi and "RSI" in df.columns else 1
    row_heights = [0.7, 0.3] if rows == 2 else [1.0]

    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
    )

    # ── OHLC 蠟燭圖 ───────────────────────────────────────────────────────────
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

    # ── 成交量柱狀圖 ──────────────────────────────────────────────────────────
    colors = ["red" if o > c else "green" for o, c in zip(df["open"], df["close"])]
    fig.add_trace(
        go.Bar(x=df.index, y=df["volume"], name="成交量", marker_color=colors, opacity=0.5),
        row=1,
        col=1,
    )

    # ── VWAP 線條 ─────────────────────────────────────────────────────────────
    if show_vwap:
        vwap_style = {
            "vwap5": ("blue", "VWAP5"),
            "vwap21": ("orange", "VWAP21"),
            "vwap55": ("red", "VWAP55"),
            "vwap144": ("purple", "VWAP144"),
        }
        for col, (color, name) in vwap_style.items():
            if col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[col],
                        mode="lines",
                        name=name,
                        line=dict(color=color, width=2),
                    ),
                    row=1,
                    col=1,
                )

    # ── RSI 子圖 ──────────────────────────────────────────────────────────────
    if rows == 2 and "RSI" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["RSI"],
                mode="lines",
                name="RSI",
                line=dict(color="purple", width=1),
            ),
            row=2,
            col=1,
        )
        # 超買/超賣水平線
        for level, color in [(70, "red"), (30, "green")]:
            fig.add_hline(y=level, line_color=color, line_dash="dash", row=2, col=1)

    fig.update_layout(
        title=f"{ticker} – OHLCV Chart",
        xaxis_rangeslider_visible=False,
        height=900,
    )

    if output_path is not None:
        output_path = Path(output_path)
        fig.write_html(str(output_path))
        logger.info("Plotly 圖表已儲存: %s", output_path)
        if open_browser:
            import webbrowser
            webbrowser.open(str(output_path))
        return output_path

    if open_browser:
        fig.show()

    return None
