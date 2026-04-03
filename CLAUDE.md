# CLAUDE.md — StockScreener

Guidance for AI assistants working on this codebase.

---

## Project Overview

A Python-based stock screening and analysis tool for identifying stocks matching technical patterns — primarily the **VCP (Volume Contraction Pattern)** and **SMA crossover strategies**. It integrates multiple financial data sources, produces interactive charts, and includes backtesting capabilities.

This is a **personal/research-grade** project. Comments are in Traditional Chinese (繁體中文). The codebase has been refactored from a flat 56-file structure into a proper Python package (`stockscreener/`).

---

## Repository Structure

```
StockScreener/
│
├── stockscreener/               ← 主套件（重構後的新架構）
│   ├── __init__.py              # 套件入口，load_config() 工具函式
│   ├── cli.py                   # CLI 入口（取代多個 main_*.py）
│   │
│   ├── data/                    # 資料取得層
│   │   ├── yahoo.py             # yfinance / yahooquery 封裝
│   │   ├── finviz.py            # FinViz screener 封裝
│   │   ├── ptp.py               # PTP 名單爬取（兩個網站合併）
│   │   ├── cache.py             # 本地 Parquet 快取
│   │   └── edgar.py             # SEC EDGAR / XBRL 封裝
│   │
│   ├── indicators/              # 技術指標計算層
│   │   ├── vwap.py              # VWAP（多視窗）
│   │   ├── sma.py               # SMA + check_continuous_increase
│   │   ├── rsi.py               # RSI
│   │   ├── zigzag.py            # Zigzag 高低點偵測
│   │   └── atr.py               # ATR
│   │
│   ├── strategies/              # 策略訊號層
│   │   ├── vcp.py               # VCP (Volume Contraction Pattern)
│   │   ├── sma_crossover.py     # SMA 21/55/155 交叉策略
│   │   └── market_status.py     # NYSE 開市狀態
│   │
│   ├── backtest/                # 回測層
│   │   ├── engine.py            # 回測核心（Strategy Pattern）
│   │   ├── position_sizing.py   # 單倉 / Pyramid 倉位管理
│   │   └── report.py            # HTML 回測報表輸出
│   │
│   ├── charts/                  # 圖表輸出層
│   │   ├── highstock.py         # Highstock OHLC + VWAP + RSI + Volume
│   │   ├── plotly_charts.py     # Plotly 互動圖表
│   │   └── heatmap.py           # Seaborn 板塊熱力圖
│   │
│   └── export/                  # 匯出層
│       └── excel.py             # Excel 輸出（openpyxl）
│
├── tests/                       # pytest 測試套件（53 個測試）
│   ├── conftest.py              # 共用 fixtures（模擬 OHLCV 資料）
│   ├── test_backtest_engine.py
│   ├── test_data_ptp.py
│   ├── test_data_yahoo.py
│   ├── test_indicators_vwap.py
│   ├── test_indicators_zigzag.py
│   └── test_strategies_vcp.py
│
├── config.yaml                  # 所有策略參數（取代 hardcoded 值）
├── pyproject.toml               # 依賴套件清單與 CLI 入口點設定
├── todo.md                      # 重寫計畫與進度追蹤
│
├── main.py                      # 原始 entry point（保留）
├── main_screener.py             # 原始最完整 screener（保留）
├── main_yfinance.py             # 原始 yfinance 版本（保留）
├── main_yahooquery.py           # 原始 yahooquery 版本（保留）
│
├── Backtest.py                  # 原始 SMA 回測（保留）
├── Backtest_pyramid.py          # 原始 Pyramid 回測（保留）
├── Backtest_pyramid_record.py   # 原始 Pyramid + 記錄（保留）
├── Backtest_wistoploss.py       # 原始止損回測（保留）
├── backtrader_2.py              # Backtrader 策略（保留）
├── backtrader回測.py            # Backtrader 策略中文檔名（保留）
│
├── is_market_open.py            # 原始開市狀態查詢（保留）
├── zigzag_plot.py               # 原始 Zigzag 圖（保留）
├── HH_LL_LH_HL.py               # Higher High/Lower Low 偵測（保留）
│
├── OK_sector_industry_volume_weight_heatmap_seaborn.py  # 保留
├── sector_industry_volume_weight_heatmap.py             # 保留
├── industry_volume_weight_heatmap_seaborn.py            # 保留
├── sector_volume_weight.py                              # 保留
├── sp500_sector.py / sp500_sector_heatmap.py            # 保留
│
├── get_finantial.py             # 財務資料擷取（保留）
├── wirte_list_to_xlsx.py        # Excel 寫入（保留）
├── py-xbrl_3.py                 # XBRL 解析（保留）
├── sec_edgar_py_test.py         # SEC EDGAR 測試（保留）
│
├── income_statement.csv         # 快取財務資料（13.2 MB）
├── data_all_financial.csv       # 聚合財務指標
├── filter_ticker.csv            # 過濾後 ticker 清單
├── Tickers.xlsx                 # 大型 ticker 資料庫（664 KB）
├── Result.xlsx                  # 回測輸出
├── industry_sector.xlsx         # 產業/板塊對應
│
└── build/                       # PyInstaller 編譯輸出
```

---

## Tech Stack

| Category | Libraries |
|----------|-----------|
| Data Fetching | `yfinance`, `yahooquery`, `finvizfinance`, `finviz.screener`, `requests`, `beautifulsoup4`, `selenium`, `sec_edgar_py` |
| Technical Analysis | `ta` (MACD, StochasticOscillator), custom VWAP/ATR/zigzag implementations |
| Backtesting | `backtrader` |
| Data Processing | `pandas`, `numpy`, `openpyxl`, `xbrl` |
| Visualization | `plotly`, `mplfinance`, `matplotlib`, `seaborn`, `python-highcharts` (Highstock) |
| Scheduling/Calendar | `pandas-market-calendars`, `pandas.tseries` |
| GUI | `PyQt5` (minimal usage) |
| Build | `PyInstaller` |

Dependencies are defined in `pyproject.toml`. Install with:
```bash
pip install -e ".[dev]"   # 含 pytest / pytest-mock
pip install -e .          # 僅生產依賴
```

---

## Key Concepts & Strategies

### VCP (Volume Contraction Pattern)
Implemented in `stockscreener/strategies/vcp.py`. Looks for stocks with:
- Volatility contraction: `volatility_8 < volatility_21 < volatility_55`
- Contraction ratio > 1.5× at each stage
- Inner volatility < 0.1
- Volume contraction: `avg_vol_8 / avg_vol_55 < 0.7`
- SMA alignment: `SMA55 > SMA144 > SMA233`
- SMA233 continuously rising for 21 days

### VWAP (Volume Weighted Average Price)
Implemented in `stockscreener/indicators/vwap.py`.
`VWAP_n = rolling_sum(close × volume, n) / rolling_sum(volume, n)`

### SMA Crossover Backtest
Implemented in `stockscreener/strategies/sma_crossover.py` + `stockscreener/backtest/`.
Buy: SMA21 crosses above SMA55, close > SMA21 > SMA55 > SMA155, all rising.
Sell: close < SMA21.

### PTP (Publicly Traded Partnership)
`stockscreener/data/ptp.py` scrapes two external sites and merges the lists.

---

## Running the Project

### 新架構 CLI（推薦）
```bash
# VCP 篩選，輸出 Highstock HTML
python -m stockscreener screen --strategy vcp

# 金字塔加碼回測
python -m stockscreener backtest --mode pyramid --balance 200000

# NYSE 開市狀態
python -m stockscreener market-status

# 板塊熱力圖
python -m stockscreener heatmap --type sector --frequency D --period 31

# 查看說明
python -m stockscreener --help
```

### 原始腳本（仍可使用）
```bash
python main_screener.py
python main.py
python Backtest.py
python is_market_open.py
```

### 測試
```bash
python -m pytest tests/ -v       # 執行全部 53 個測試
python -m pytest tests/ -v -k vcp  # 只跑 VCP 相關測試
```

### Build
```bash
pyinstaller main.spec
```

---

## Code Conventions

### Language
- Code comments are in **Traditional Chinese (繁體中文)** — do not translate.
- Function and variable names use **snake_case**.

### DataFrame Column Naming
- All internal DataFrames use **lowercase** column names: `open`, `high`, `low`, `close`, `volume`.
- `stockscreener/data/yahoo.py::normalize_columns()` converts yfinance's capitalized names on input.

### Logging
- Package code uses `logger = logging.getLogger(__name__)` — no bare `print()`.
- CLI (`cli.py`) may use `print()` for user-facing output.

### Style
- `pd.options.mode.chained_assignment = None` at script top (original scripts)
- `today = str(datetime.datetime.now().date())`
- Procedural style; classes used only in backtest layer
- Long functions are common in original scripts — do not refactor unless asked

### Configuration
- All hardcoded thresholds/URLs/parameters live in `config.yaml`.
- Load via `stockscreener.load_config()` which returns a dict.

---

## Testing

```bash
python -m pytest tests/ -v
```

53 tests covering:
- `test_backtest_engine.py` — BacktestEngine, FixedSizing, PyramidSizing
- `test_data_ptp.py` — PTP HTML parsing, deduplication, remove logic
- `test_data_yahoo.py` — column normalization, MultiIndex selection
- `test_indicators_vwap.py` — VWAP calculation correctness
- `test_indicators_zigzag.py` — zigzag alternation, empty data handling
- `test_strategies_vcp.py` — VCP conditions, edge cases

All tests use mocks — no real network calls.

---

## External Data Sources & Rate Limits

| Source | Library | Notes |
|--------|---------|-------|
| Yahoo Finance | `yfinance` | May rate-limit; add `time.sleep()` between batches |
| Yahoo Query | `yahooquery` | Async-capable; handles multiple tickers in one call |
| FinViz | `finvizfinance` | Scraping-based; use sparingly |
| SEC EDGAR | `sec_edgar_py` | Public API; rate limits apply |
| TradingView | `selenium` | Requires Chrome + ChromeDriver |
| Wikipedia | `requests` + `bs4` | S&P 500 list scraping |
| PTP Lists | `requests` + `bs4` | Two external sites |

---

## Output Files

Scripts generate output in the working directory:
- **HTML files** — Interactive Highstock or Plotly charts
- **PNG/JPG files** — Static matplotlib/seaborn charts
- **Excel files** — `Result.xlsx`, updated `Tickers.xlsx`
- **CSV files** — Incremental data snapshots

---

## Known Limitations & Gotchas

1. **pyproject.toml** defines dependencies but no lockfile exists — versions may drift.
2. **Large CSV files** — `income_statement.csv` (13.2 MB), `Tickers.xlsx` (664 KB) committed to repo.
3. **PyInstaller build** — `build/` directory contains compiled artifacts. Do not commit changes there.
4. **Chinese filenames** — `backtrader回測.py` contains Chinese characters.
5. **No credentials management** — TradingView credentials hardcoded in `tradingview_login.py`.
6. **Rate limiting** — Yahoo Finance and FinViz can ban IPs. Code lacks retry/backoff.
7. **numpy bool** — `vcp_screener_strategy()` explicitly returns `bool()` to handle NumPy 2.0 breaking change where `np.bool_` is no longer a subclass of Python `bool`.

---

## Git Workflow

- Default development branch: `main`
- Feature branches: `claude/<description>-<id>`
- No CI/CD pipeline

---

## What NOT To Do

- Do not reorganize files into subdirectories without explicit request
- Do not add type annotations or docstrings to original scripts that don't have them
- Do not translate Chinese comments to English
- Do not modify dated backup files (`main_bak*.py`, `*_20231028.xlsx`)
- Do not add logging frameworks or abstract error handling to original ad-hoc scripts
- Do not refactor original long functions unless the task explicitly requires it
- Do not commit large data files (`.csv`, `.xlsx`) unless they already exist in the repo
