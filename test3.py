import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from plotly.subplots import make_subplots
ticker = 'AAPL'
#df = yf.download(symbol, start='2020-01-01')
df = yf.download(ticker, period='1y', interval='1d')


# first declare an empty figure
fig = go.Figure()
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[0.5,0.1])

# removing all empty dates
# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

# add OHLC
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             showlegend=False)
              )


# add moving averages to df
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA5'] = df['Close'].rolling(window=5).mean()

# add VCMA to df
df['total_price'] = df['Close'] * df['Volume']
df['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
df['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
df['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
df['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

# add moving average traces
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma5'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='VCMA 5'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma21'],
                         opacity=0.7,
                         line=dict(color='green', width=2),
                         name='VCMA 21'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma55'],
                         opacity=0.7,
                         line=dict(color='red', width=2),
                         name='VCMA 55'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma144'],
                         opacity=0.7,
                         line=dict(color='magenta', width=2),
                         name='VCMA 144'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma233'],
                         opacity=0.7,
                         line=dict(color='goldenrod', width=2),
                         name='VCMA 233'))

# hide dates with no values
fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
# remove rangeslider
fig.update_layout(xaxis_rangeslider_visible=False)
# add chart title
fig.update_layout(title="AAPL")

colors = ['green' if row['Open'] - row['Close'] >= 0
          else 'red' for index, row in df.iterrows()]
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     marker_color=colors
                    ), row=2, col=1)


# removing white space
fig.update_layout(margin=go.layout.Margin(
        l=20, #left margin
        r=20, #right margin
        b=20, #bottom margin
        t=40  #top margin
    ))

fig.write_image("fig1.jpeg")

fig.show()