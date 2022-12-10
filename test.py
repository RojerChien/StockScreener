import yfinance as yf
import test2.graph_objects as go
from test2.subplots import make_subplots

ticker = 'AAPL'
data = yf.download(tickers=ticker, period='1y', interval='1d')
print(data)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
               vertical_spacing=0.03, subplot_titles=(ticker, 'Volume'),
               row_width=[0.2, 0.7])
#fig = make_subplots(specs=[[{"secondary_y": True}]])
#fig = go.Figure(data=[go.Candlestick(x=data.index,
#                                     open=data['Open'],
#                                     high=data['High'],
#                                     low=data['Low'],
#                                     close=data['Close'])])
fig.add_trace(go.Candlestick(x=data.index,
                                    open=data['Open'],
                                    high=data['High'],
                                    low=data['Low'],
                                    close=data['Close'],
                                    name=ticker),
                                    #secondary_y=True
                                    row=1, col=1
)
#fig.add_trace(go.Bar(x=data.index, y=data['Volume'], showlegend=False), row=2, col=1,secondary_y=False)
fig.add_trace(go.Bar(x=data.index, y=data['Volume'], showlegend=False), row=2, col=1)
#fig.layout.yaxis2.showgrid=False
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()
