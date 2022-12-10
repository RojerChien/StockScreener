

#import pandas_ta as ta
#from ta.trend import MACD
#from ta.momentum import StochasticOscillator



fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[0.5,0.1])

colors = ['green' if row['Open'] - row['Close'] >= 0
          else 'red' for index, row in df.iterrows()]
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     marker_color=colors
                    ), row=2, col=1)

fig = go.Figure(go.Candlestick(x=df.index,
  open=df['Open'],
  high=df['High'],
  low=df['Low'],
  close=df['Close']))

# removing rangeslider
fig.update_layout(xaxis_rangeslider_visible=False)
# hide weekends
fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
# removing all empty dates
# build complete timeline from start date to end date
dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
# retrieve the dates that ARE in the original datset
dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
# define dates with missing values
dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

# add moving averages to df
df['total_price'] = df['Close'] * df['Volume']
df['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
df['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
df['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
df['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma5'],
                         opacity=0.7,
                         line=dict(color='blue', width=2),
                         name='VCMA 5'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma21'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='VCMA 21'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma55'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='VCMA 55'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma144'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='VCMA 144'))
fig.add_trace(go.Scatter(x=df.index,
                         y=df['vcma233'],
                         opacity=0.7,
                         line=dict(color='orange', width=2),
                         name='VCMA 233'))

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[0.5,0.1])


# add chart title
# Plot volume trace on 2nd row
#fig = make_subplots(rows=2, cols=1, shared_xaxes=True)



"""
fig.update_layout(height=900, width=1200,
                  showlegend=False,
                  xaxis_rangeslider_visible=False,
                  xaxis_rangebreaks=[dict(values=dt_breaks)])
# add subplot properties when initializing fig variable
fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[0.5,0.1,0.2,0.2])
# update y-axis label
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)
"""
#fig.update_layout(title=ticker)
fig.show()