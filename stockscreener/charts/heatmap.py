"""stockscreener.charts.heatmap – S&P 500 sector/industry volume-weight heatmap.

Logic from OK_sector_industry_volume_weight_heatmap_seaborn.py:
1. Get S&P 500 list from Wikipedia
2. Group by GICS Sector and GICS Sub-Industry
3. Download OHLCV data for all S&P 500 stocks (yfinance)
4. Calculate volume per period (daily/weekly/monthly) per sector
5. Calculate percentage of total volume per sector/industry
6. Plot seaborn heatmap with plasma colormap, annotate with .1% format
7. Also plot per-sector industry bar charts with % labels
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

__all__ = ["render_sector_heatmap"]

_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def _get_sp500_table() -> pd.DataFrame:
    """從 Wikipedia 取得 S&P 500 公司列表。"""
    tables = pd.read_html(_SP500_URL)
    sp500_table = tables[0]
    # 將 BRK.B 等包含 '.' 的 ticker 轉換為 yfinance 格式（BRK-B）
    sp500_table["Symbol"] = sp500_table["Symbol"].str.replace(".", "-", regex=False)
    return sp500_table


def render_sector_heatmap(
    frequency: str = "D",
    time_value: int = 31,
    colormap: str = "plasma",
    figsize: tuple = (20, 10),
    output_dir: str | Path = ".",
    save_fig: bool = True,
    show_fig: bool = True,
    show_industry_bars: bool = True,
) -> Optional[Path]:
    """繪製 S&P 500 各板塊成交量佔比熱力圖。

    Parameters
    ----------
    frequency:
        時間頻率：``'D'``（日）、``'W'``（週）、``'M'``（月）。
    time_value:
        回溯期間數量，例如頻率為 ``'D'`` 時代表天數。
    colormap:
        seaborn 色板，預設 ``'plasma'``。
    figsize:
        圖表尺寸 (寬, 高)，預設 ``(20, 10)``。
    output_dir:
        輸出目錄，預設當前目錄。
    save_fig:
        是否儲存圖表為 PNG，預設 ``True``。
    show_fig:
        是否顯示圖表，預設 ``True``。
    show_industry_bars:
        是否產生各板塊的子產業條形圖，預設 ``True``。

    Returns
    -------
    Path or None
        若 *save_fig* 為 ``True`` 則回傳儲存的 PNG 路徑，否則 ``None``。
    """
    import datetime

    import matplotlib.pyplot as plt  # type: ignore
    import seaborn as sns  # type: ignore
    import yfinance as yf  # type: ignore
    from dateutil.relativedelta import relativedelta  # type: ignore
    from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, USFederalHolidayCalendar  # type: ignore
    from pandas.tseries.offsets import CustomBusinessDay  # type: ignore

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── 取得 S&P 500 名單 ─────────────────────────────────────────────────────
    logger.info("取得 S&P 500 公司列表...")
    sp500_table = _get_sp500_table()
    sectors = sp500_table["GICS Sector"].unique()
    industry_groups = sp500_table["GICS Sub-Industry"].unique()

    stocks_by_sector = {
        sector: sp500_table[sp500_table["GICS Sector"] == sector]["Symbol"].tolist()
        for sector in sectors
    }
    stocks_by_industry_group = {
        ig: sp500_table[sp500_table["GICS Sub-Industry"] == ig]["Symbol"].tolist()
        for ig in industry_groups
    }

    # ── 計算日期範圍 ───────────────────────────────────────────────────────────
    today = datetime.datetime.today()
    freq_map = {"D": "days", "W": "weeks", "M": "months"}
    if frequency not in freq_map:
        raise ValueError(f"無效的 frequency：{frequency}，請使用 'D'、'W' 或 'M'")

    kwargs = {freq_map[frequency]: time_value}
    start_date = today - relativedelta(**kwargs)
    end_date = today

    class _CustomHolidayCalendar(AbstractHolidayCalendar):
        rules = [
            Holiday("New Year Holiday", month=1, day=2),
            Holiday("Martin Luther King Jr. Day", month=1, day=16),
            Holiday("Washington Day", month=2, day=20),
            Holiday("Good Friday", month=4, day=7),
            Holiday("Memorial Day", month=5, day=29),
            Holiday("Juneteenth", month=6, day=19),
            Holiday("Independence Day", month=7, day=4),
            Holiday("Labor Day", month=9, day=4),
            Holiday("Thanksgiving Day", month=11, day=23),
            Holiday("Christmas Day", month=12, day=25),
        ]

    custom_bd = CustomBusinessDay(calendar=_CustomHolidayCalendar())
    pd_freq = custom_bd if frequency == "D" else ("W" if frequency == "W" else "ME")
    date_range = pd.date_range(start_date, end_date, freq=pd_freq)

    # ── 下載所有股票資料 ──────────────────────────────────────────────────────
    all_stocks = sp500_table["Symbol"].tolist()
    logger.info("下載 %d 檔股票資料...", len(all_stocks))
    all_stock_data = yf.download(all_stocks, start=start_date, end=end_date, group_by="ticker", progress=False)

    # ── 計算各期間總成交量與板塊/子產業成交量 ─────────────────────────────────
    weekly_total_volume = []
    weekly_volume_by_sector = {sector: [] for sector in sectors}
    weekly_volume_by_industry_group = {ig: [] for ig in industry_groups}

    for start, end in zip(date_range[:-1], date_range[1:]):
        week_total = 0
        for stock in all_stocks:
            try:
                vol = all_stock_data[stock]["Volume"].loc[start:end].sum()
                week_total += vol
            except (KeyError, TypeError):
                pass
        weekly_total_volume.append(week_total)

        for sector, stocks in stocks_by_sector.items():
            sector_vol = 0
            for stock in stocks:
                try:
                    sector_vol += all_stock_data[stock]["Volume"].loc[start:end].sum()
                except (KeyError, TypeError):
                    pass
            weekly_volume_by_sector[sector].append(sector_vol)

        for ig, stocks in stocks_by_industry_group.items():
            ig_vol = 0
            for stock in stocks:
                try:
                    ig_vol += all_stock_data[stock]["Volume"].loc[start:end].sum()
                except (KeyError, TypeError):
                    pass
            weekly_volume_by_industry_group[ig].append(ig_vol)

    # ── 計算百分比 ────────────────────────────────────────────────────────────
    weekly_pct_by_sector = {
        sector: [
            vol / total if total != 0 else 0
            for vol, total in zip(week_vols, weekly_total_volume)
        ]
        for sector, week_vols in weekly_volume_by_sector.items()
    }
    weekly_pct_by_industry_group = {
        ig: [
            vol / total if total != 0 else 0
            for vol, total in zip(week_vols, weekly_total_volume)
        ]
        for ig, week_vols in weekly_volume_by_industry_group.items()
    }

    percentage_df = pd.DataFrame(weekly_pct_by_sector).T
    percentage_df.columns = [d.strftime("%Y-%m-%d") for d in date_range[:-1]]

    # ── 繪製熱力圖 ────────────────────────────────────────────────────────────
    plt.figure(figsize=figsize)
    sns.heatmap(
        percentage_df,
        annot=True,
        fmt=".1%",
        cmap=colormap,
        linewidths=0.5,
        annot_kws={"size": 8},
    )
    plt.title("Sector Volume Percentage")
    plt.xticks(rotation=45)

    output_path: Optional[Path] = None
    if save_fig:
        output_path = output_dir / "sector_heatmap.png"
        plt.savefig(output_path, bbox_inches="tight")
        logger.info("熱力圖已儲存: %s", output_path)

    if show_fig:
        plt.show()
    plt.close()

    # ── 各板塊子產業條形圖 ────────────────────────────────────────────────────
    if show_industry_bars and len(date_range) > 1:
        last_idx = len(date_range) - 2  # 最後一個期間
        for sector in sectors:
            igs_in_sector = sp500_table[sp500_table["GICS Sector"] == sector]["GICS Sub-Industry"].unique()
            ig_pcts = [
                weekly_pct_by_industry_group[ig][last_idx]
                if last_idx < len(weekly_pct_by_industry_group.get(ig, []))
                else 0
                for ig in igs_in_sector
            ]
            ig_df = pd.DataFrame({"Industry Group": igs_in_sector, "Percentage": ig_pcts})

            import matplotlib.pyplot as plt
            import seaborn as sns
            plt.figure(figsize=(20, 10))
            ax = sns.barplot(x="Industry Group", y="Percentage", data=ig_df, palette="viridis")
            plt.title(f"{sector} Industry Group Percentage")
            plt.xticks(rotation=90, fontsize=8)
            plt.ylabel("Percentage")
            for p in ax.patches:
                ax.annotate(
                    f"{p.get_height():.2%}",
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="baseline",
                    fontsize=9,
                    color="black",
                    xytext=(0, 3),
                    textcoords="offset points",
                )
            if save_fig:
                bar_path = output_dir / f"R_{sector.replace(' ', '_')}.png"
                plt.savefig(bar_path, bbox_inches="tight")
            if show_fig:
                plt.show()
            plt.close()

    logger.info("熱力圖繪製完成")
    return output_path
