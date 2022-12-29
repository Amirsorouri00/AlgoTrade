import pandas as pd
import yfinance as yf

cryptocurrency = 'ETH-BTC'

df = yf.download(cryptocurrency, period='1y')
df.dropna(inplace=True)

date = []
open = []
high = []
low = []
close = []

# for i in range(len(df)):
date.append(df.index)
open.append(df['Open'])
high.append(df['High'])
low.append(df['Low'])
close.append(df['Close'])

# print(date, open, high, low, close)


date_df = pd.DataFrame(date).rename(columns={0: 'Date'})
open_df = pd.DataFrame(open).rename(columns={0: 'Open'})
# print(date_df)
high_df = pd.DataFrame(high).rename(columns={0: 'High'})
low_df = pd.DataFrame(low).rename(columns={0: 'Low'})
close_df = pd.DataFrame(close).rename(columns={0: 'Close'})
# frames = [date_df, open_df, high_df, low_df, close_df]
frames = [df['Open'], df['Close'], df['High'], df['Low']]
df = pd.concat(frames, axis=1, join='inner')

print(df)
