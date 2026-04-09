"""stockscreener.cli - 命令列入口（取代多個 main_*.py）。

使用方式：
    python -m stockscreener screen --strategy vcp
    python -m stockscreener backtest --mode pyramid
    python -m stockscreener market-status
    python -m stockscreener heatmap --type sector
"""

from __future__ import annotations

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=level,
    )


def cmd_screen(args: argparse.Namespace) -> None:
    """執行股票篩選（VCP 或 VWAP 策略）。"""
    from stockscreener.data.ptp import get_ptp_tickers, remove_ptp_tickers
    from stockscreener.data.finviz import get_finviz_screener_tickers
    from stockscreener.data.yahoo import get_yq_historical_data, sel_yq_historical_data
    from stockscreener.strategies.vcp import vcp_screener_strategy
    from stockscreener.charts.highstock import render_highstock_chart
    from stockscreener.indicators.vwap import add_all_vwaps
    from stockscreener.indicators.rsi import calculate_rsi

    print(f"[screen] 策略: {args.strategy}, 範圍: {args.universe}, 輸出: {args.output}")

    # ── 取得股票範圍 ──────────────────────────────────────────────────────────
    if args.universe == "russell1000":
        from stockscreener.data.russell import get_russell1000_tickers
        print("取得 Russell 1000 成分股（iShares IWB）...")
        try:
            tickers = get_russell1000_tickers()
        except (ConnectionError, ValueError) as exc:
            print(f"[錯誤] {exc}")
            return
    else:
        print("取得 FinViz Screener tickers...")
        tickers = get_finviz_screener_tickers()

    if not args.skip_ptp:
        print("取得 PTP 名單並過濾...")
        ptp = get_ptp_tickers()
        tickers = remove_ptp_tickers(ptp, tickers)

    print(f"共 {len(tickers)} 支股票進入篩選")
    data_all = get_yq_historical_data(tickers)

    matched = []
    for ticker in tickers:
        df = sel_yq_historical_data(data_all, ticker)
        if df.empty:
            continue
        if args.strategy == "vcp":
            if vcp_screener_strategy(ticker, df):
                matched.append(ticker)
                if args.output in ("html", "both"):
                    url = f"https://www.tradingview.com/chart/sWFIrRUP/?symbol={ticker}"
                    df = add_all_vwaps(df)
                    df["RSI"] = calculate_rsi(df, 14)
                    render_highstock_chart(df, ticker, tradingview_url=url)

    print(f"\n篩選完畢，共 {len(matched)} 支符合條件: {matched}")


def cmd_backtest(args: argparse.Namespace) -> None:
    """執行回測（單倉或金字塔加碼）。"""
    import pandas as pd
    from stockscreener.data.yahoo import get_yq_historical_data, sel_yq_historical_data
    from stockscreener.strategies.sma_crossover import sma_crossover_signals
    from stockscreener.backtest.engine import BacktestEngine
    from stockscreener.backtest.position_sizing import pyramid_sizing, fixed_sizing
    from stockscreener.backtest.report import generate_html_report as render_backtest_html

    if args.tickers:
        symbols = [t.strip() for t in args.tickers.split(",")]
    else:
        print("取得 S&P 500 列表...")
        sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        try:
            tables = pd.read_html(sp500_url)
            symbols = [s.replace(".", "-") for s in tables[0]["Symbol"].tolist()]
        except Exception as exc:
            print(f"[錯誤] 無法取得 S&P 500 列表: {exc}")
            print("請改用 --tickers 指定股票，例如：")
            print("  python -m stockscreener backtest --mode pyramid --tickers AAPL,TSLA,NVDA")
            return

    print(f"下載 {len(symbols)} 支股票資料...")
    try:
        data_all = get_yq_historical_data(symbols)
    except ConnectionError as exc:
        print(f"[錯誤] {exc}")
        return

    sizing_fn = pyramid_sizing if args.mode == "pyramid" else fixed_sizing
    engine = BacktestEngine(
        signal_fn=sma_crossover_signals,
        sizing_fn=sizing_fn,
        initial_balance=args.balance,
    )

    results = []
    for symbol in symbols:
        df = sel_yq_historical_data(data_all, symbol)
        if df.empty:
            continue
        try:
            result = engine.run(df, ticker=symbol)
            results.append(result)
        except Exception as exc:
            logger.warning("回測 %s 失敗: %s", symbol, exc)

    print(f"回測完成，共 {len(results)} 支股票")
    output_file = render_backtest_html(results, output_path=f"backtest_{args.mode}.html")
    print(f"報表已儲存: {output_file}")


def cmd_market_status(_args: argparse.Namespace) -> None:
    """顯示 NYSE 目前開市狀態。"""
    from stockscreener.strategies.market_status import check_market_status

    is_open, is_within_hours, time_since_open, time_until_close, time_until_open = (
        check_market_status()
    )

    if is_open:
        print("市場目前開市中")
        print(f"  開市後經過: {time_since_open}")
        print(f"  距離收盤: {time_until_close}")
    else:
        print("市場目前休市")
        if time_until_open is not None:
            print(f"  距離開市: {time_until_open}")


def cmd_heatmap(args: argparse.Namespace) -> None:
    """產生板塊 / 產業熱力圖。"""
    from stockscreener.charts.heatmap import render_sector_heatmap

    print(f"[heatmap] 類型: {args.type}, 頻率: {args.frequency}, 期間: {args.period}")
    render_sector_heatmap(
        heatmap_type=args.type,
        frequency=args.frequency,
        time_value=args.period,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stockscreener",
        description="股票篩選、回測與視覺化工具",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="顯示 DEBUG 訊息")
    sub = parser.add_subparsers(dest="command", required=True)

    # screen
    p_screen = sub.add_parser("screen", help="股票篩選")
    p_screen.add_argument("--strategy", choices=["vcp", "vwap"], default="vcp")
    p_screen.add_argument("--output", choices=["html", "csv", "both"], default="html")
    p_screen.add_argument(
        "--universe",
        choices=["finviz", "russell1000"],
        default="finviz",
        help="篩選範圍：finviz（FinViz Screener）或 russell1000（Russell 1000 成分股）",
    )
    p_screen.add_argument("--skip-ptp", action="store_true")
    p_screen.set_defaults(func=cmd_screen)

    # backtest
    p_bt = sub.add_parser("backtest", help="策略回測")
    p_bt.add_argument("--mode", choices=["single", "pyramid"], default="pyramid")
    p_bt.add_argument("--start", default="2007-01-01")
    p_bt.add_argument("--end", default=None)
    p_bt.add_argument("--balance", type=float, default=200_000.0)
    p_bt.add_argument("--tickers", default=None)
    p_bt.set_defaults(func=cmd_backtest)

    # market-status
    p_ms = sub.add_parser("market-status", help="NYSE 開市狀態")
    p_ms.set_defaults(func=cmd_market_status)

    # heatmap
    p_hm = sub.add_parser("heatmap", help="板塊 / 產業熱力圖")
    p_hm.add_argument("--type", choices=["sector", "industry"], default="sector")
    p_hm.add_argument("--frequency", choices=["D", "W", "M"], default="D")
    p_hm.add_argument("--period", type=int, default=31)
    p_hm.set_defaults(func=cmd_heatmap)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(getattr(args, "verbose", False))
    args.func(args)


if __name__ == "__main__":
    main()
