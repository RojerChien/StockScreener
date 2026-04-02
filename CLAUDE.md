# CLAUDE.md — StockScreener

Guidance for AI assistants working on this codebase.

---

## Project Overview

A Python-based stock screening and analysis tool for identifying stocks matching technical patterns — primarily the **VCP (Volume Contraction Pattern)** and **SMA crossover strategies**. It integrates multiple financial data sources, produces interactive charts, and includes backtesting capabilities.

This is a **personal/research-grade** project: flat file structure, exploratory coding style, comments in Traditional Chinese (繁體中文), and multiple experimental variants.

---

## Repository Structure

```
StockScreener/
├── main.py                          # Entry point: PTP filtering, VWAP charting, Highstock output
├── main_screener.py                 # Most complete screener: FinViz + VCP strategy (1478 lines)
├── main_yfinance.py                 # Alternative using yfinance + zigzag support/resistance
├── main_yahooquery.py               # Alternative using yahooquery + income statement data
├── main_backup.py                   # Backup snapshots (do not use as canonical)
├── main_bak20231010.py              # Dated backup
├── main_optimized.py                # Experimental optimized version
│
├── Backtest.py                      # SMA 21/55/155 crossover strategy backtest
├── Backtest_pyramid.py              # Pyramid position sizing strategy
├── Backtest_pyramid_record.py       # Pyramid strategy with full trade recording
├── Backtest_wistoploss.py           # Strategy with stop-loss + trailing stop
├── backtrader_2.py                  # Backtrader-based strategy
├── backtrader回測.py                # Backtrader strategy (Chinese-named file)
│
├── is_market_open.py                # NYSE market status checker
├── zigzag_plot.py                   # Zigzag pattern detection (peaks/valleys)
├── zigzag_my.py / zigzag_my_2.py   # Custom zigzag implementations
├── HH_LL_LH_HL.py                  # Higher High/Lower Low pattern detection
│
├── OK_sector_industry_volume_weight_heatmap_seaborn.py  # Sector/industry heatmaps
├── sector_industry_volume_weight_heatmap.py
├── industry_volume_weight_heatmap_seaborn.py
├── sector_volume_weight.py
├── sp500_sector.py / sp500_sector_heatmap.py
│
├── get_finantial.py                 # Financial statement + XBRL data fetching
├── wirte_list_to_xlsx.py            # Write ticker data to Excel (872 lines)
├── py-xbrl.py / py-xbrl_2.py / py-xbrl_3.py  # XBRL/SEC EDGAR parsing
├── sec_edgar_py_test.py             # SEC EDGAR wrapper testing
│
├── chrome_driver.py                 # Selenium WebDriver setup
├── tradingview_login.py             # TradingView authentication
├── highchart_to_png.py              # Highstock chart export to PNG
├── combine_jpg.py                   # Image manipulation utility
├── read_xlsx_to_list.py             # Excel reading utility
├── remove_file.py                   # File cleanup utility
├── python_gui.py                    # Minimal PyQt5 GUI stub
│
├── test.py / test2.py / test3.py / test4.py   # Ad-hoc test scripts
├── yahoo_query_test.py              # yahooquery data fetch tests
├── yfinance_test.py / yahooquery_test.py / finvizfinance_test.py
├── update_income_statement_test.py
│
├── income_statement.csv             # Cached financial data (13.2 MB)
├── data_all_financial.csv           # Aggregated financial metrics
├── filter_ticker.csv                # Filtered ticker list
├── tsla_data.csv                    # Tesla historical sample
├── yq_historical.csv                # yahooquery historical data
├── Tickers.xlsx                     # Large ticker database (664 KB)
├── Result.xlsx                      # Backtest output
├── industry_sector.xlsx             # Industry/sector mapping
│
├── main.spec                        # PyInstaller build config
└── build/                           # PyInstaller compiled output
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

**No `requirements.txt` exists.** Dependencies must be inferred from imports.

---

## Key Concepts & Strategies

### VCP (Volume Contraction Pattern)
The primary screening strategy. Looks for stocks with:
- Price above SMA20 > SMA50 > SMA200
- Decreasing volume over successive bases (contraction)
- EPS growth criteria
- Price > $3, daily volume > 100K shares
- Daily change > 2%

### VWAP (Volume Weighted Average Price)
Used as a key indicator in `main.py` and `main_screener.py`. VWAP lines are computed from intraday data and overlaid on Highstock interactive charts.

### SMA Crossover Backtest
`Backtest.py` tests SMA 21/55/155 crossovers on the S&P 500. Pyramid variants apply risk-scaled position sizing with stop-loss rules.

### PTP (Passive Foreign Investment Company / "PTP" stocks)
`main.py` scrapes PTP stock lists from external websites and filters them out of screening results to avoid tax complications.

---

## Data Flow

```
External APIs (Yahoo Finance, FinViz, SEC EDGAR)
        ↓
  Data Fetching (yfinance / yahooquery / finvizfinance)
        ↓
  Filtering & Technical Indicators (pandas / ta / custom)
        ↓
  Strategy Signal Generation (VCP / SMA crossover / Zigzag)
        ↓
  Visualization (Highstock HTML / Plotly / Matplotlib / Seaborn)
        ↓
  Export (Excel / CSV / PNG / HTML charts)
```

---

## Running the Project

There is no build system or package manager. Run scripts directly:

```bash
# Primary screener
python main_screener.py

# VWAP + Highstock charts
python main.py

# Alternative screener (yfinance)
python main_yfinance.py

# Market open check
python is_market_open.py

# Backtesting
python Backtest.py
python Backtest_pyramid_record.py

# Build standalone executable
pyinstaller main.spec
```

---

## Code Conventions

### Language
- Code comments and some variable names are in **Traditional Chinese (繁體中文)**. This is intentional — do not translate them.
- Function and variable names use **snake_case** in Python.

### Style Patterns
- Warnings suppressed at script top: `pd.options.mode.chained_assignment = None`
- Today's date stored as: `today = str(datetime.datetime.now().date())`
- `import` blocks sometimes include commented `pip install` instructions
- Procedural style dominates; classes are rarely used
- Long functions (100+ lines) are common — do not refactor for style alone

### Column Naming
- Yahoo Finance columns use capitalized names: `Close`, `Volume`, `Open`, `High`, `Low`
- yahooquery may return lowercase: `close`, `volume`
- Be careful when merging DataFrames from different sources

### File Organization
- All `.py` files live in the root directory — **no package/module structure**
- `main_*.py` files are parallel implementations; `main_screener.py` is the most complete
- Files prefixed with `test` or `*_test.py` are ad-hoc validation scripts, not a test suite
- Backup files with dates (`main_bak20231010.py`) are archived — do not modify them

---

## Testing

There is **no formal test framework**. Testing is done by running individual scripts and inspecting output.

To validate a data source:
```bash
python yfinance_test.py
python yahooquery_test.py
python finvizfinance_test.py
```

When adding new features, follow the pattern: create a `_test.py` variant script and run it manually.

---

## External Data Sources & Rate Limits

| Source | Library | Notes |
|--------|---------|-------|
| Yahoo Finance | `yfinance` | May rate-limit on bulk requests; add `time.sleep()` between batches |
| Yahoo Query | `yahooquery` | Async-capable; handles multiple tickers in one call |
| FinViz | `finvizfinance` | Scraping-based; use sparingly |
| SEC EDGAR | `sec_edgar_py` | Public API; no auth required but rate limits apply |
| TradingView | `selenium` | Requires Chrome + ChromeDriver; login credentials needed |
| Wikipedia | `requests` + `bs4` | S&P 500 list scraping |
| PTP Lists | `requests` + `bs4` | Two external sites scraped for PTP ticker exclusion |

---

## Output Files

Scripts generate output in the working directory:
- **HTML files** — Interactive Highstock or Plotly charts (open in browser)
- **PNG/JPG files** — Static matplotlib/seaborn charts
- **Excel files** — `Result.xlsx`, updated `Tickers.xlsx`
- **CSV files** — Incremental data snapshots

There is no output directory convention — files land in the project root.

---

## Known Limitations & Gotchas

1. **No `requirements.txt`** — If dependencies are missing, check imports at the top of each file for `pip install` hints in comments.
2. **Flat file structure** — All 56+ Python files are in the root. Search by filename prefix to find related files.
3. **Multiple `main_*.py` variants** — They are NOT interchangeable. Each uses a different data source and has different feature sets.
4. **Large CSV files** — `income_statement.csv` (13.2 MB) and `Tickers.xlsx` (664 KB) are committed to the repo. Avoid rewriting these unless specifically asked.
5. **PyInstaller build** — The `build/` directory contains compiled artifacts. Do not commit changes there.
6. **Chinese filenames** — `backtrader回測.py` contains Chinese characters. Ensure your shell/editor handles UTF-8 filenames.
7. **No environment variables** — API keys or credentials (TradingView) are hardcoded in scripts. Do not commit new credentials.
8. **Rate limiting** — Yahoo Finance and FinViz can ban IPs on excessive requests. The code lacks robust retry/backoff logic.

---

## Git Workflow

- Default development branch: `main`
- Feature branches follow pattern: `claude/<description>-<id>`
- No CI/CD pipeline; commits and pushes are manual
- No pre-commit hooks or linting enforced

---

## What NOT To Do

- Do not reorganize files into subdirectories without explicit request — the flat structure is intentional for this scripting project
- Do not add type annotations or docstrings to existing code that doesn't have them
- Do not translate Chinese comments to English
- Do not create a `requirements.txt` unless asked — the current state is deliberate
- Do not modify dated backup files (`main_bak*.py`, `*_20231028.xlsx`)
- Do not add logging frameworks or abstract error handling to ad-hoc scripts
- Do not refactor long functions unless the task explicitly requires it
