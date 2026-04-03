"""stockscreener.charts.highstock – Highstock OHLCV + VWAP + RSI chart renderer.

Chart layout (original main_screener.py):
  - OHLC candlestick  (70% height), red down / green up
  - Volume column     (13% height, top 72%), red if open > close else green
  - RSI line          (13% height, top 87%), plotLines at 30 and 70
  - VWAP lines: 5 (blue), 21 (orange), 55 (red), 144 (purple), lineWidth=3
  - Toggle VWAP button (JavaScript)
  - TradingView link as subtitle
  - rangeSelector selected: 4
  - Tooltip shows OHLC + 漲跌幅 (change %)
Output: save as {ticker}_{date}.html and webbrowser.open()
"""

from __future__ import annotations

import datetime
import logging
import webbrowser
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["render_highstock_chart"]

_TODAY = str(datetime.datetime.now().date())

# VWAP 線條顏色設定
_VWAP_COLORS = {5: "blue", 21: "orange", 55: "red", 144: "purple"}
_VWAP_LINE_WIDTH = 3


def _add_vwap_to_chart(chart, df: pd.DataFrame, window: int, color: str, line_width: int, vwap_id: str) -> None:
    """將指定 VWAP 加入 Highstock 圖表。"""
    col = f"vwap{window}"
    if col not in df.columns:
        return

    vwap_data = [
        [int(pd.Timestamp(df.index[i]).value // 10**6), round(float(v), 2)]
        for i, v in enumerate(df[col].values)
        if not pd.isna(v)
    ]

    # 重建完整序列（含 None for NaN）以保持時間對齊
    vwap_data = [
        [int(pd.Timestamp(df.index[i]).value // 10**6),
         round(float(df[col].iloc[i]), 2) if not pd.isna(df[col].iloc[i]) else None]
        for i in range(len(df))
    ]

    chart.add_data_set(
        vwap_data,
        "line",
        f"vwap{window}",
        yAxis=0,
        color=color,
        lineWidth=line_width,
        id=vwap_id,
        dataGrouping={"units": [["day", [1]]]},
    )


def render_highstock_chart(
    df: pd.DataFrame,
    ticker: str,
    tradingview_url: str = "",
    date: str = _TODAY,
    output_dir: str | Path = ".",
    open_browser: bool = True,
) -> Path:
    """產生 Highstock OHLCV + VWAP + RSI 互動式 HTML 圖表。

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
        TradingView 連結 URL（顯示於副標題）。
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
        from highcharts import Highstock  # type: ignore
    except ImportError:
        logger.error("python-highcharts 未安裝，無法產生 Highstock 圖表")
        raise

    chart = Highstock(renderTo="container", width=None, height=930)

    # ── RSI ──────────────────────────────────────────────────────────────────
    if "RSI" in df.columns:
        rsi_data = [
            [int(pd.Timestamp(df.index[i]).value // 10**6), round(float(r), 2)]
            for i, r in enumerate(df["RSI"].values)
        ]
        chart.add_data_set(rsi_data, "line", "RSI", yAxis=2, dataGrouping={"units": [["day", [1]]]})

    # ── 成交量 10 日均線 ───────────────────────────────────────────────────────
    df = df.copy()
    df["volume_10ma"] = df["volume"].rolling(window=10).mean()
    volume_10ma_data = [
        [int(pd.Timestamp(df.index[i]).value // 10**6), float(v) if not pd.isna(v) else None]
        for i, v in enumerate(df["volume_10ma"].values)
    ]
    chart.add_data_set(
        volume_10ma_data,
        "line",
        "10日成交量移動平均",
        yAxis=1,
        dataGrouping={"units": [["day", [1]]]},
    )

    # ── OHLC 蠟燭圖 ───────────────────────────────────────────────────────────
    ohlc_data = [
        [
            int(pd.Timestamp(df.index[i]).value // 10**6),
            round(float(o), 2),
            round(float(h), 2),
            round(float(l), 2),
            round(float(c), 2),
        ]
        for i, (o, h, l, c) in enumerate(df[["open", "high", "low", "close"]].values)
    ]
    chart.add_data_set(ohlc_data, "candlestick", ticker, dataGrouping={"units": [["day", [1]]]})

    # ── VWAP 線條（由長到短，確保短線在上層）─────────────────────────────────
    for window, color in [(144, "purple"), (55, "red"), (21, "orange"), (5, "blue")]:
        _add_vwap_to_chart(chart, df, window, color, _VWAP_LINE_WIDTH, f"vwap{window}")

    # ── 成交量柱狀圖 ──────────────────────────────────────────────────────────
    volume_data = [
        {
            "x": int(pd.Timestamp(df.index[i]).value // 10**6),
            "y": float(v),
            "color": "red" if float(o) > float(c) else "green",
        }
        for i, (o, c, v) in enumerate(df[["open", "close", "volume"]].values)
    ]
    chart.add_data_set(volume_data, "column", "成交量", yAxis=1, dataGrouping={"enabled": False})

    # ── 圖表設定 ──────────────────────────────────────────────────────────────
    toggle_js = """
        function () {
            var chart = this;
            var toggleVwapLines = function () {
                var vwap144 = chart.get('vwap144'),
                    vwap55  = chart.get('vwap55'),
                    vwap21  = chart.get('vwap21'),
                    vwap5   = chart.get('vwap5');
                if (vwap144 && vwap144.visible) {
                    vwap144.hide(); vwap55.hide(); vwap21.hide(); vwap5.hide();
                } else {
                    if (vwap144) vwap144.show();
                    if (vwap55)  vwap55.show();
                    if (vwap21)  vwap21.show();
                    if (vwap5)   vwap5.show();
                }
            };
            chart.renderer.button('Toggle VWAP Lines', null, null, toggleVwapLines)
                .attr({ zIndex: 3 }).add();
        }
    """

    subtitle_html = (
        f'<a href="{tradingview_url}" target="_blank" '
        f'style="color: #003399; text-decoration: underline; cursor: pointer;">TradingView</a>'
        if tradingview_url
        else ""
    )

    options = {
        "chart": {"events": {"load": toggle_js}},
        "navigation": {
            "buttonOptions": {"align": "right", "verticalAlign": "top", "y": 0}
        },
        "rangeSelector": {"selected": 4},
        "title": {"text": f"{ticker} ({date})"},
        "subtitle": {
            "text": subtitle_html,
            "useHTML": True,
            "align": "center",
            "y": 35,
        },
        "yAxis": [
            {
                "labels": {"align": "right", "x": -3},
                "title": {"text": "OHLC"},
                "height": "70%",
                "lineWidth": 2,
            },
            {
                "labels": {"align": "right", "x": -3},
                "title": {"text": "成交量"},
                "top": "72%",
                "height": "13%",
                "offset": 0,
                "lineWidth": 2,
            },
            {
                "labels": {"align": "right", "x": -3},
                "title": {"text": "RSI"},
                "top": "87%",
                "height": "13%",
                "offset": 0,
                "lineWidth": 2,
                "plotLines": [
                    {"value": 30, "color": "#FF4500", "width": 1},
                    {"value": 70, "color": "#FF4500", "width": 1},
                ],
            },
        ],
        "tooltip": {
            "formatter": f"""
                function () {{
                    var dataIndex = this.points[0].point.index;
                    var s = '<b>' + Highcharts.dateFormat('%A, %b %e, %Y', this.x) + '</b>';
                    s += '<br/>';
                    this.points.forEach(function (point) {{
                        if (point.series.name === '{ticker}') {{
                            s += '<br/>' + point.series.name + ': ';
                            s += 'Open: ' + point.point.open.toFixed(2);
                            s += ', High: ' + point.point.high.toFixed(2);
                            s += ', Low: ' + point.point.low.toFixed(2);
                            s += ', Close: ' + point.point.close.toFixed(2);
                            var change = 0;
                            if (dataIndex > 0) {{
                                var previousClose = point.series.options.data[dataIndex - 1][4];
                                change = ((point.point.close - previousClose) / previousClose) * 100;
                            }}
                            s += '<br/>漲跌幅: ' + change.toFixed(2) + '%';
                        }} else {{
                            s += '<br/>' + point.series.name + ': ' + point.y;
                        }}
                    }});
                    return s;
                }}
            """
        },
        "plotOptions": {
            "line": {"showInLegend": True},
            "candlestick": {"color": "red", "upColor": "green"},
            "column": {"borderColor": "none"},
        },
    }

    chart.set_dict_options(options)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"{ticker}_{date}.html"

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(chart.htmlcontent)

    logger.info("Highstock 圖表已儲存: %s", filename)

    if open_browser:
        webbrowser.open(str(filename))

    return filename
