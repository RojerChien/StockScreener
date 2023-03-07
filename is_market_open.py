import pandas_market_calendars as mcal
import pandas_market_calendars as mcal
import datetime
import pandas as pd
import pytz

nyse = mcal.get_calendar('NYSE')

def check_market_status():
    now = datetime.datetime.now(tz=pytz.timezone('America/New_York')).replace(microsecond=0)
    schedule = nyse.schedule(start_date=now.date(), end_date=now.date())

    if len(schedule) == 0:
        # The market is currently closed
        return False, False, None, None

    market_open = schedule.loc[schedule.index[0], 'market_open'].tz_convert('America/New_York')
    market_close = schedule.loc[schedule.index[0], 'market_close'].tz_convert('America/New_York')

    if market_open <= now <= market_close:
        # It is market hours now
        is_market_open = True
        is_within_market_hours = True
        time_since_open = now - market_open
        time_until_close = market_close - now
        time_until_open = None
    else:
        # It is not market hours now
        is_market_open = False
        is_within_market_hours = False
        time_since_open = None
        #time_until_close = None if now >= market_close else market_open - now
        time_until_open = (market_open - now) if not is_market_open else None
        time_until_close = market_open - now if is_within_market_hours else None
        #time_until_open = market_close - now if not is_market_open else None

    return is_market_open, is_within_market_hours, time_since_open, time_until_close, time_until_open

is_market_open, is_within_market_hours, time_since_open, time_until_close, time_until_open = check_market_status()
#total_time = time_until_close + time_until_open
print(is_market_open)
print(is_within_market_hours)
print(time_since_open)
print(time_until_close)
print(time_until_open)
#print(total_time)

if not is_market_open:
    print('The market is currently closed.')
    print(f'Time until open: {time_until_open}')
elif is_within_market_hours:
    print('The market is currently open.')
    print(f'Time since open: {time_since_open}')
    print(f'Time until close: {time_until_close}')

#else:
#   print('The market is not open yet.')
#  print(f'Time until open: {time_until_open}')


"""import pandas_market_calendars as mcal
import datetime
import pandas as pd
import pytz


def is_market_open():
    # 取得 NYSE 行事曆
    nyse = mcal.get_calendar('NYSE')

    # 取得現在的時間（紐約時區）
    now_ny = datetime.datetime.now(tz=pytz.timezone('America/New_York')).replace(microsecond=0)
    now_utc = now_ny.astimezone(pytz.utc)
    now_ts = pd.to_datetime(now_utc.strftime('%Y-%m-%d %H:%M:%S+00:00'))
    now_date = now_ny.date()

    # 取得近 5 天內的 NYSE 行事曆
    days_ago = now_date - datetime.timedelta(days=5)
    days_later = now_date + datetime.timedelta(days=5)
    schedule = nyse.schedule(start_date=days_ago, end_date=days_later)

    # 取得 NYSE 行事曆內的開市時間和收市時間
    market_open = schedule.loc[schedule.index[0], 'market_open'].tz_convert('America/New_York')
    market_close = schedule.loc[schedule.index[0], 'market_close'].tz_convert('America/New_York')

    # 判斷現在是否為開市時間
    is_open = market_open <= now_ts <= market_close

    # 判斷今天是否為開市日
    first_date = schedule.index[0].date()
    last_date = schedule.index[-1].date()
    date_range = pd.date_range(start=first_date, end=last_date, freq='D').date
    is_today_open = now_date in date_range

    # 回傳是否為開市時間和是否為開市日的布林值
    return is_open, is_today_open

result1, result2 = is_market_open()
if not result1 and result2:
    print('The market is closed now, and will open later today.')
elif result1 and result2:
    print('The market is open now, and it is market hours.')
else:
    print('The market is open today.')

"""



#print(result)

"""import pandas_market_calendars as mcal
import datetime
import pandas as pd
import pytz

nyse = mcal.get_calendar('NYSE')

days_ago = datetime.date.today() - datetime.timedelta(days=5)
days_later = datetime.date.today() + datetime.timedelta(days=5)
now_date = datetime.datetime.now(tz=pytz.timezone('America/New_York')).replace(microsecond=0).date()
now = datetime.datetime.now(tz=pytz.timezone('America/New_York')).replace(microsecond=0)

now_utc = now.astimezone(pytz.utc)
now_str = now_utc.strftime('%Y-%m-%d %H:%M:%S+00:00')
now_ts = pd.to_datetime(now_str)
schedule = nyse.schedule(start_date=days_ago, end_date=days_later)

first_date = schedule.index[0].date()
last_date = schedule.index[-1].date()
date_range = pd.date_range(start=first_date, end=last_date, freq='D').date

market_open = schedule.loc[schedule.index[0], 'market_open'].tz_convert('America/New_York')
market_close = schedule.loc[schedule.index[0], 'market_close'].tz_convert('America/New_York')
is_open = market_open <= now_ts <= market_close

if now_date in date_range:
    if is_open:
        print('The market is open today, and it is market hours now.')
    else:
        print('The market is open today, but it is NOT market hours now.')
else:
    print('The market is currently closed')

#print('NYSE is closed today')

#print(market_open)
#print(market_close)
#print(now_ts)





#first_date = schedule.head(1)
#first_date_1 = first_date.loc[first_date.index[0]]
#print(first_date)
#print(last_date)
#print(first_date_1)



#date_range =  pd.date_range()

#if now_date in date_range

#market_open = schedule.at[1, 'market_open']

#market_open = schedule.loc[schedule.index[0], 'market_open']
#market_close = schedule.loc[schedule.index[0], 'market_close']
#print(now_str)

#market_open = schedule.at[0, 'market_open']
#market_close = schedule.at[0, 'market_close']

"""