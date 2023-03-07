import pandas_market_calendars as mcal
import datetime
import pandas as pd
import pytz

nyse = mcal.get_calendar('NYSE')

now = datetime.datetime.now(tz=pytz.timezone('America/New_York')).replace(microsecond=0)

now_utc = now.astimezone(pytz.utc)
now_str = now_utc.strftime('%Y-%m-%d %H:%M:%S+00:00')
now_ts = pd.to_datetime(now_str)
schedule = nyse.schedule(start_date=now.date(), end_date=now.date())
#market_open = schedule.at[1, 'market_open']
print(schedule)
#market_open = schedule.loc[schedule.index[0], 'market_open']
#market_close = schedule.loc[schedule.index[0], 'market_close']
#print(now_str)

#market_open = schedule.at[0, 'market_open']
#market_close = schedule.at[0, 'market_close']

#print('NYSE is closed today')
market_open = schedule.loc[schedule.index[0], 'market_open'].tz_convert('America/New_York')
market_close = schedule.loc[schedule.index[0], 'market_close'].tz_convert('America/New_York')

print(market_open)
print(market_close)
print(now_ts)

is_open = market_open <= now_ts <= market_close

if is_open:
    print('The market is currently open')
else:
    print('The market is currently closed')