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

Note: HTML is generated directly without python-highcharts to ensure
compatibility with Python 3.10+ (python-highcharts uses deprecated
collections.Iterable removed in Python 3.10).
"""

from __future__ import annotations

import datetime
import json
import logging
import webbrowser
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["render_highstock_chart"]

_TODAY = str(datetime.datetime.now().date())

# VWAP 線條顏色設定
_VWAP_COLORS = {5: "blue", 21: "orange", 55: "red", 144: "purple"}
_VWAP_LINE_WIDTH = 3


def _ts_ms(ts) -> int:
    """將 pandas Timestamp 轉為毫秒 Unix 時間戳。"""
    return int(pd.Timestamp(ts).value // 10**6)


def _build_ohlc_data(df: pd.DataFrame) -> list:
    return [
        [_ts_ms(df.index[i]),
         round(float(df["open"].iloc[i]), 2),
         round(float(df["high"].iloc[i]), 2),
         round(float(df["low"].iloc[i]), 2),
         round(float(df["close"].iloc[i]), 2)]
        for i in range(len(df))
    ]


def _build_volume_data(df: pd.DataFrame) -> list:
    return [
        {"x": _ts_ms(df.index[i]),
         "y": float(df["volume"].iloc[i]),
         "color": "red" if float(df["open"].iloc[i]) > float(df["close"].iloc[i]) else "green"}
        for i in range(len(df))
    ]


def _build_volume_ma_data(df: pd.DataFrame) -> list:
    vol_ma = df["volume"].rolling(window=10).mean()
    return [
        [_ts_ms(df.index[i]),
         round(float(vol_ma.iloc[i]), 2) if not pd.isna(vol_ma.iloc[i]) else None]
        for i in range(len(df))
    ]


def _build_rsi_data(df: pd.DataFrame) -> list:
    return [
        [_ts_ms(df.index[i]), round(float(df["RSI"].iloc[i]), 2)]
        for i in range(len(df))
        if not pd.isna(df["RSI"].iloc[i])
    ]


def _build_vwap_data(df: pd.DataFrame, window: int) -> list:
    col = f"vwap{window}"
    if col not in df.columns:
        return []
    return [
        [_ts_ms(df.index[i]),
         round(float(df[col].iloc[i]), 2) if not pd.isna(df[col].iloc[i]) else None]
        for i in range(len(df))
    ]


def _build_html(
    ticker: str,
    date: str,
    tradingview_url: str,
    ohlc_data: list,
    volume_data: list,
    volume_ma_data: list,
    rsi_data: list,
    vwap_series: list,
) -> str:
    """將資料序列化為 Highstock HTML 字串。"""

    ohlc_json = json.dumps(ohlc_data)
    volume_json = json.dumps(volume_data)
    volume_ma_json = json.dumps(volume_ma_data)
    rsi_json = json.dumps(rsi_data)

    subtitle_html = (
        f'<a href="{tradingview_url}" target="_blank" '
        f'style="color:#003399;text-decoration:underline;cursor:pointer;">TradingView</a>'
        if tradingview_url else ""
    )

    # 建立 VWAP series JS 物件
    vwap_series_js_parts = []
    for w, color, data in vwap_series:
        vwap_series_js_parts.append(
            f"""{{
                type: 'line',
                name: 'vwap{w}',
                id: 'vwap{w}',
                data: {json.dumps(data)},
                yAxis: 0,
                color: '{color}',
                lineWidth: {_VWAP_LINE_WIDTH},
                dataGrouping: {{ units: [['day', [1]]] }}
            }}"""
        )
    vwap_series_js = ",\n".join(vwap_series_js_parts)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>{ticker} ({date})</title>
<script src="https://code.highcharts.com/stock/highstock.js"></script>
<script src="https://code.highcharts.com/stock/modules/data.js"></script>
<script src="https://code.highcharts.com/stock/modules/exporting.js"></script>
<style>
  html, body {{ margin: 0; padding: 0; }}
  #container {{ width: 100%; height: 930px; }}
</style>
</head>
<body>
<div id="container"></div>
<script>
(function () {{
  var ohlcData     = {ohlc_json};
  var volumeData   = {volume_json};
  var volumeMaData = {volume_ma_json};
  var rsiData      = {rsi_json};

  Highcharts.stockChart('container', {{
    chart: {{
      events: {{
        load: function () {{
          var chart = this;
          chart.renderer.button('Toggle VWAP Lines', 10, 10, function () {{
            var ids = ['vwap144', 'vwap55', 'vwap21', 'vwap5'];
            var first = chart.get(ids[0]);
            if (!first) return;
            var show = !first.visible;
            ids.forEach(function (id) {{
              var s = chart.get(id);
              if (s) {{ show ? s.show() : s.hide(); }}
            }});
          }}).attr({{ zIndex: 3 }}).add();
        }}
      }}
    }},
    navigation: {{
      buttonOptions: {{ align: 'right', verticalAlign: 'top', y: 0 }}
    }},
    rangeSelector: {{ selected: 4 }},
    title: {{ text: '{ticker} ({date})' }},
    subtitle: {{
      text: '{subtitle_html}',
      useHTML: true,
      align: 'center',
      y: 35
    }},
    yAxis: [
      {{
        labels: {{ align: 'right', x: -3 }},
        title: {{ text: 'OHLC' }},
        height: '70%',
        lineWidth: 2
      }},
      {{
        labels: {{ align: 'right', x: -3 }},
        title: {{ text: '成交量' }},
        top: '72%',
        height: '13%',
        offset: 0,
        lineWidth: 2
      }},
      {{
        labels: {{ align: 'right', x: -3 }},
        title: {{ text: 'RSI' }},
        top: '87%',
        height: '13%',
        offset: 0,
        lineWidth: 2,
        plotLines: [
          {{ value: 30, color: '#FF4500', width: 1 }},
          {{ value: 70, color: '#FF4500', width: 1 }}
        ]
      }}
    ],
    tooltip: {{
      formatter: function () {{
        var dataIndex = this.points[0].point.index;
        var s = '<b>' + Highcharts.dateFormat('%A, %b %e, %Y', this.x) + '</b>';
        this.points.forEach(function (point) {{
          if (point.series.name === '{ticker}') {{
            s += '<br/>' + point.series.name + ': ';
            s += 'Open: ' + point.point.open.toFixed(2);
            s += ', High: ' + point.point.high.toFixed(2);
            s += ', Low: ' + point.point.low.toFixed(2);
            s += ', Close: ' + point.point.close.toFixed(2);
            var change = 0;
            if (dataIndex > 0) {{
              var prevClose = ohlcData[dataIndex - 1][4];
              change = ((point.point.close - prevClose) / prevClose) * 100;
            }}
            s += '<br/>漲跌幅: ' + change.toFixed(2) + '%';
          }} else {{
            s += '<br/>' + point.series.name + ': ' + (point.y !== null ? point.y : 'N/A');
          }}
        }});
        return s;
      }}
    }},
    plotOptions: {{
      line: {{ showInLegend: true }},
      candlestick: {{ color: 'red', upColor: 'green' }},
      column: {{ borderColor: 'none' }}
    }},
    series: [
      {{
        type: 'candlestick',
        name: '{ticker}',
        data: ohlcData,
        dataGrouping: {{ units: [['day', [1]]] }}
      }},
      {{
        type: 'column',
        name: '成交量',
        data: volumeData,
        yAxis: 1,
        dataGrouping: {{ enabled: false }}
      }},
      {{
        type: 'line',
        name: '10日成交量移動平均',
        data: volumeMaData,
        yAxis: 1,
        dataGrouping: {{ units: [['day', [1]]] }}
      }},
      {{
        type: 'line',
        name: 'RSI',
        data: rsiData,
        yAxis: 2,
        dataGrouping: {{ units: [['day', [1]]] }}
      }},
      {vwap_series_js}
    ]
  }});
}})();
</script>
</body>
</html>"""
    return html


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
    df = df.copy()

    ohlc_data = _build_ohlc_data(df)
    volume_data = _build_volume_data(df)
    volume_ma_data = _build_volume_ma_data(df)
    rsi_data = _build_rsi_data(df) if "RSI" in df.columns else []

    # VWAP series（由長到短）
    vwap_series = []
    for window, color in [(144, "purple"), (55, "red"), (21, "orange"), (5, "blue")]:
        data = _build_vwap_data(df, window)
        if data:
            vwap_series.append((window, color, data))

    html_content = _build_html(
        ticker=ticker,
        date=date,
        tradingview_url=tradingview_url,
        ohlc_data=ohlc_data,
        volume_data=volume_data,
        volume_ma_data=volume_ma_data,
        rsi_data=rsi_data,
        vwap_series=vwap_series,
    )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"{ticker}_{date}.html"

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(html_content)

    logger.info("Highstock 圖表已儲存: %s", filename)

    if open_browser:
        webbrowser.open(str(filename))

    return filename
