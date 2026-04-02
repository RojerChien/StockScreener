"""stockscreener.strategies.market_status – NYSE market status checker."""

from __future__ import annotations

import datetime
import logging
from typing import Optional, Tuple

import pytz

logger = logging.getLogger(__name__)

__all__ = ["check_market_status"]

_TIMEZONE = "America/New_York"
_CALENDAR = "NYSE"


def check_market_status() -> Tuple[bool, bool, Optional[datetime.timedelta], Optional[datetime.timedelta], Optional[datetime.timedelta]]:
    """判斷目前 NYSE 是否在交易時間內。

    Returns
    -------
    tuple
        (is_market_open, is_within_market_hours, time_since_open,
         time_until_close, time_until_open)

        - ``is_market_open``: 目前是否在交易時間
        - ``is_within_market_hours``: 同上（兩者相同，保持與原始碼一致）
        - ``time_since_open``: 距離開市的時間差（開市中時有值）
        - ``time_until_close``: 距離收市的時間差（開市中時有值）
        - ``time_until_open``: 距離下次開市的時間差（收市時有值）
    """
    import pandas_market_calendars as mcal  # type: ignore

    nyse = mcal.get_calendar(_CALENDAR)
    now = datetime.datetime.now(tz=pytz.timezone(_TIMEZONE)).replace(microsecond=0)
    schedule = nyse.schedule(start_date=now.date(), end_date=now.date())

    if len(schedule) == 0:
        # 今天市場未開市（假日或週末）
        return False, False, None, None, None

    market_open = schedule.loc[schedule.index[0], "market_open"].tz_convert(_TIMEZONE)
    market_close = schedule.loc[schedule.index[0], "market_close"].tz_convert(_TIMEZONE)

    if market_open <= now <= market_close:
        # 目前在交易時間內
        is_market_open = True
        is_within_market_hours = True
        time_since_open = now - market_open
        time_until_close = market_close - now
        time_until_open = None
    else:
        # 目前不在交易時間
        is_market_open = False
        is_within_market_hours = False
        time_since_open = None
        time_until_close = None
        time_until_open = (market_open - now) if now < market_open else None

    return is_market_open, is_within_market_hours, time_since_open, time_until_close, time_until_open
