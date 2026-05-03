# 重寫計畫 (Rewrite Plan)

保留所有現有功能，以更清晰的結構、可維護性與可測試性重寫整個專案。

---

## 核心問題分析 (Current Problems)

| 問題 | 說明 |
|------|------|
| 平坦結構 | 56+ 個 `.py` 全部放在根目錄，難以導覽 |
| 重複程式碼 | `get_ptp_tickers`、`add_vwap_to_chart`、`highchart_chart` 在 `main.py`/`main_screener.py`/`main_yahooquery.py` 重複出現 |
| 無 `requirements.txt` | 依賴套件全靠記憶，換機器必出錯 |
| 設定值寫死 | FinViz 篩選條件、VWAP 週期、SMA 參數全部 hardcoded 在函式內 |
| 全域變數 | `today`、`true_number` 散落在 module 頂層 |
| 無錯誤處理 | 外部 API 呼叫無 retry/fallback，一旦失敗整個腳本崩潰 |
| 無快取 | 每次執行都重新打 API，速度慢且容易被封鎖 |
| 無測試框架 | `test.py`、`test2.py` 是手動驗證腳本，不可自動執行 |
| 到處用 `print` | 無法調整 log level，debug 訊息與重要輸出混在一起 |
| Dead code | `get_ptp_tickers` 中 `return` 之後還有 `print(ptp_lists)`（永遠不執行） |
| 欄位命名不一致 | `yfinance` 用 `Close`，`yahooquery` 用 `close`，混用時出 KeyError |
| 多個回測實作 | `Backtest.py`、`Backtest_pyramid.py`、`Backtest_pyramid_record.py` 邏輯高度重疊但各自獨立 |

---

## 目標架構 (Target Architecture)

```
stockscreener/                  ← Python package 根目錄
│
├── pyproject.toml              ← 依賴管理（取代手動 pip 安裝）
├── config.yaml                 ← 策略參數、API 設定（取代 hardcoded 值）
│
├── stockscreener/              ← 主套件
│   ├── __init__.py
│   │
│   ├── data/                   ← 資料取得層
│   │   ├── __init__.py
│   │   ├── yahoo.py            ← yfinance / yahooquery 封裝
│   │   ├── finviz.py           ← FinViz screener 封裝
│   │   ├── edgar.py            ← SEC EDGAR / XBRL 封裝
│   │   ├── ptp.py              ← PTP 名單爬取
│   │   └── cache.py            ← 本地快取（Parquet 或 SQLite）
│   │
│   ├── indicators/             ← 技術指標計算層
│   │   ├── __init__.py
│   │   ├── vwap.py             ← VWAP（各週期）
│   │   ├── sma.py              ← SMA 21/55/155/200
│   │   ├── rsi.py              ← RSI
│   │   ├── zigzag.py           ← Zigzag 高低點偵測
│   │   └── atr.py              ← ATR
│   │
│   ├── strategies/             ← 策略訊號層
│   │   ├── __init__.py
│   │   ├── vcp.py              ← VCP（Volume Contraction Pattern）
│   │   ├── sma_crossover.py    ← SMA 21/55/155 交叉策略
│   │   └── market_status.py    ← NYSE 開市狀態
│   │
│   ├── backtest/               ← 回測層
│   │   ├── __init__.py
│   │   ├── engine.py           ← 回測核心引擎（共用邏輯）
│   │   ├── position_sizing.py  ← 單倉 / Pyramid 部位管理
│   │   └── report.py           ← 回測結果輸出（HTML、Excel）
│   │
│   ├── charts/                 ← 圖表輸出層
│   │   ├── __init__.py
│   │   ├── highstock.py        ← Highstock OHLC + VWAP + RSI + Volume
│   │   ├── plotly_charts.py    ← Plotly 互動圖表
│   │   └── heatmap.py          ← Seaborn 板塊熱力圖
│   │
│   ├── export/                 ← 匯出層
│   │   ├── __init__.py
│   │   ├── excel.py            ← Excel 輸出（openpyxl）
│   │   └── html.py             ← HTML 報表
│   │
│   └── cli.py                  ← CLI 入口（取代多個 main_*.py）
│
├── tests/                      ← pytest 測試
│   ├── test_data_yahoo.py
│   ├── test_data_ptp.py
│   ├── test_indicators_vwap.py
│   ├── test_indicators_zigzag.py
│   ├── test_strategies_vcp.py
│   ├── test_backtest_engine.py
│   └── conftest.py             ← 共用 fixtures（mock API 回應）
│
└── output/                     ← 產出檔案目錄（HTML、PNG、Excel）
```

---

## TODO 清單

### Phase 1 — 基礎建設

- [ ] **1.1** 建立 `pyproject.toml`（或 `requirements.txt`），列出所有依賴套件與版本
  - `pandas`, `numpy`, `yfinance`, `yahooquery`, `finvizfinance`, `finviz`
  - `ta`, `mplfinance`, `plotly`, `matplotlib`, `seaborn`, `python-highcharts`
  - `pandas-market-calendars`, `openpyxl`, `beautifulsoup4`, `requests`
  - `sec_edgar_py`, `xbrl`, `selenium`, `PyQt5`, `backtrader`
  - `pytest`, `pytest-mock`（開發依賴）

- [ ] **1.2** 建立套件目錄結構（所有 `__init__.py`）

- [ ] **1.3** 建立 `config.yaml`，將以下 hardcoded 值移出程式碼：
  ```yaml
  finviz_filters:
    sma: "SMA20 above SMA50"
    avg_volume: "Over 100K"
    price: "Over $3"
    eps_growth: "Positive (>0%)"
    change: "Up 2%"

  vwap_windows: [5, 21, 55, 144]

  sma_periods: [21, 55, 155, 200]

  backtest:
    initial_balance: 200000
    pyramid_ratios: [0.1, 0.50, 1.0]
    pyramid_thresholds: [0.0, 0.03, 0.06]

  data:
    default_period: "3y"
    default_interval: "1d"
    cache_dir: "cache/"
  ```

- [ ] **1.4** 設定 `logging`，以 `logger = logging.getLogger(__name__)` 取代所有 `print`

---

### Phase 2 — 資料層 (`stockscreener/data/`)

- [ ] **2.1** `ptp.py` — 整合 `get_ptp_tickers` + `remove_ptp_list`
  - 修正 dead code（`return` 後的 `print`）
  - 加入 requests `timeout` 與錯誤處理
  - 加入快取（當天抓過就不重抓）

- [ ] **2.2** `yahoo.py` — 統一 `yfinance` 與 `yahooquery` 介面
  - 解決欄位命名不一致問題：輸出統一使用小寫 `open/high/low/close/volume`
  - 加入 retry 邏輯（指數退避，最多 4 次）
  - 加入 batch size 限制，避免被 Yahoo 封鎖

- [ ] **2.3** `finviz.py` — 封裝 `get_finviz_screener_tickers`
  - 篩選條件從 `config.yaml` 讀取

- [ ] **2.4** `cache.py` — 本地 Parquet 快取
  - 依 ticker + 日期命名快取檔案
  - 快取過期邏輯（例如：當天的資料不重抓）

- [ ] **2.5** `edgar.py` — 封裝 `sec_edgar_py` + `xbrl` 邏輯（從 `get_finantial.py`、`py-xbrl*.py` 整合）

---

### Phase 3 — 指標層 (`stockscreener/indicators/`)

- [ ] **3.1** `vwap.py` — 提取 `add_vwap_to_chart` 中的 VWAP 計算邏輯
  - 輸入：OHLCV DataFrame + window
  - 輸出：帶 `vwap{window}` 欄位的 DataFrame

- [ ] **3.2** `sma.py` — SMA 計算，支援多週期
  - 輸入：close Series + periods list
  - 輸出：帶 `sma_{period}` 欄位的 DataFrame

- [ ] **3.3** `rsi.py` — RSI 計算（目前散落在各 main 檔）

- [ ] **3.4** `zigzag.py` — 整合 `zigzag_plot.py`、`zigzag_my.py`、`zigzag_my_2.py` 為單一實作

- [ ] **3.5** `atr.py` — ATR 計算（目前在 `main_yfinance.py`）

---

### Phase 4 — 策略層 (`stockscreener/strategies/`)

- [ ] **4.1** `vcp.py` — 提取 `vcp_screener_strategy` 函式
  - 輸入：單一 ticker 的 OHLCV DataFrame
  - 輸出：`bool`（是否符合 VCP 條件）
  - 條件來自 `config.yaml`

- [ ] **4.2** `sma_crossover.py` — SMA 21/55/155 交叉訊號生成
  - 輸入：OHLCV DataFrame
  - 輸出：buy/sell signal series

- [ ] **4.3** `market_status.py` — 整合 `is_market_open.py`（清除多個被 `"""` 包住的廢棄實作）

---

### Phase 5 — 回測層 (`stockscreener/backtest/`)

- [ ] **5.1** `engine.py` — 共用回測核心（合併 `Backtest.py`、`Backtest_pyramid.py`、`Backtest_pyramid_record.py` 的重複邏輯）
  - 接受策略函式作為參數（Strategy Pattern）
  - 接受部位管理函式作為參數

- [ ] **5.2** `position_sizing.py` — 兩種模式：
  - `single` — 固定資金比例
  - `pyramid` — 三段進場（10% / 50% / 100%，門檻 0% / 3% / 6%）

- [ ] **5.3** `report.py` — 回測結果輸出
  - 單一函式產生 HTML（DataTables 排序）
  - 支援 trade records 與 summary 兩種格式

---

### Phase 6 — 圖表層 (`stockscreener/charts/`)

- [ ] **6.1** `highstock.py` — 整合 `highchart_chart` 函式（目前重複在 3 個主檔）
  - OHLC + VWAP(5/21/55/144) + Volume + RSI
  - Toggle VWAP button（JavaScript 邏輯保留）
  - VWAP 週期從 `config.yaml` 讀取

- [ ] **6.2** `plotly_charts.py` — 整合 `test2.py`、`test3.py` 的 Plotly 圖表

- [ ] **6.3** `heatmap.py` — 整合 `OK_sector_industry_volume_weight_heatmap_seaborn.py`、`industry_volume_weight_heatmap_seaborn.py`、`sector_volume_weight.py`

---

### Phase 7 — CLI 入口 (`stockscreener/cli.py`)

取代多個 `main_*.py`，以 CLI 參數選擇功能：

```bash
# 執行 VCP 篩選（Highstock 圖表輸出）
python -m stockscreener screen --strategy vcp --output html

# 執行回測
python -m stockscreener backtest --mode pyramid --start 2007-01-01 --end 2024-01-01

# 查看市場狀態
python -m stockscreener market-status

# 產生板塊熱力圖
python -m stockscreener heatmap --type sector
```

- [ ] **7.1** 使用 `argparse` 或 `click` 建立 CLI
- [ ] **7.2** 保留 PyInstaller 相容性（更新 `main.spec`）

---

### Phase 8 — 測試 (`tests/`)

- [ ] **8.1** `conftest.py` — 建立 mock fixtures（避免測試時真的打外部 API）
  - Mock `yfinance.download`
  - Mock `yahooquery.Ticker`
  - Mock `requests.get`（PTP 頁面）

- [ ] **8.2** `test_data_ptp.py`
  - 測試 HTML 解析邏輯（用 fixture HTML 字串）
  - 測試兩個 PTP 來源合併與去重

- [ ] **8.3** `test_indicators_vwap.py`
  - 測試 VWAP 計算結果（用已知數據驗算）

- [ ] **8.4** `test_indicators_zigzag.py`
  - 測試高低點偵測邏輯

- [ ] **8.5** `test_strategies_vcp.py`
  - 測試 VCP 條件判斷（符合 / 不符合 各一個 case）

- [ ] **8.6** `test_backtest_engine.py`
  - 測試單倉與 pyramid 部位大小計算
  - 測試 buy/sell 訊號配對邏輯

---

### Phase 9 — 清理

- [ ] **9.1** 刪除以下不再需要的檔案（確認功能已遷移後）：
  - `main_backup.py`、`main_bak20231010.py`、`main_optimized.py`、`main_screener_backup_20230507`
  - `test.py`、`test2.py`、`test3.py`、`test4.py`、`test_everything.py`
  - `yahoo_query_test.py`、`yfinance_test.py`、`yahooquery_test.py`、`finvizfinance_test.py`
  - `zigzag_my.py`、`zigzag_my_2.py`（整合到 `indicators/zigzag.py` 後）
  - `py-xbrl.py`、`py-xbrl_2.py`（整合到 `data/edgar.py` 後）

- [ ] **9.2** 將 `income_statement.csv`（13.2 MB）、`Tickers.xlsx`（664 KB）移到 `data/` 目錄並加入 `.gitignore`

- [ ] **9.3** 更新 `CLAUDE.md` 反映新架構

---

## 優先順序建議

```
Phase 1（基礎建設）→ Phase 2（資料層）→ Phase 3（指標層）
       ↓                                        ↓
Phase 7（CLI）  ←────────────── Phase 4（策略層）
       ↓
Phase 5（回測層）+ Phase 6（圖表層）[可平行進行]
       ↓
Phase 8（測試）→ Phase 9（清理）
```

Phase 1~3 是核心，其他 Phase 依賴它們。Phase 5 與 Phase 6 互相獨立，可以同時進行。

---

## 不需要改動的項目

- 所有中文注解 — 保留原樣
- 對外 API 呼叫邏輯（`yfinance`、`yahooquery`、FinViz 的呼叫方式本身沒問題）
- Highstock 的 JavaScript Toggle VWAP 邏輯
- DataTables HTML 回測報表格式
- PyInstaller 建置目標（保留 `main.spec`，更新入口點即可）
