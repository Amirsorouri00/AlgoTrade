import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from termcolor import colored as cl

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


def get_historic_data(symbol):
    cryptocurrency_df = yf.download(symbol, period='1y')
    cryptocurrency_df.dropna(inplace=True)
    df = cryptocurrency_df
    frames = [df['Open'], df['Close'], df['High'], df['Low']]
    df = pd.concat(frames, axis=1, join='inner')
    return df


cryptocurrency = 'ETH-BTC'
ETH_BTC = get_historic_data(cryptocurrency)
ETH_BTC.index = pd.to_datetime(ETH_BTC.index)

plt.plot(ETH_BTC.index, ETH_BTC['Close'])
plt.xlabel('Date')
plt.ylabel('Closing Prices')
plt.title('ETH_BTC Stock Prices 2020-2021')
plt.show()


def sma(data, window):
    sma = data.rolling(window=window).mean()
    return sma


ETH_BTC['sma_30'] = sma(ETH_BTC['Close'], 30)
print(ETH_BTC.tail())

ETH_BTC['Close'].plot(label='CLOSE', alpha=0.6)
ETH_BTC['sma_30'].plot(label='SMA 30', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Closing Prices')
plt.legend(loc='upper left')
plt.show()


def bb(data, sma, window, coeff=2):
    std = data.rolling(window=window).std()
    upper_bb = sma + std * coeff
    lower_bb = sma - std * coeff
    return upper_bb, lower_bb


ETH_BTC['upper_bb1'], ETH_BTC['lower_bb1'] = bb(
    ETH_BTC['Close'], ETH_BTC['sma_30'], 30, 1)
ETH_BTC['upper_bb'], ETH_BTC['lower_bb'] = bb(
    ETH_BTC['Close'], ETH_BTC['sma_30'], 30)
ETH_BTC['upper_bb3'], ETH_BTC['lower_bb3'] = bb(
    ETH_BTC['Close'], ETH_BTC['sma_30'], 30, 3)
print(ETH_BTC.tail())

ETH_BTC['Close'].plot(label='CLOSE PRICES', color='skyblue')
ETH_BTC['upper_bb1'].plot(label='UPPER BB 10', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['upper_bb'].plot(label='UPPER BB 20', linestyle='--',
                         linewidth=1, color='black')
ETH_BTC['upper_bb3'].plot(label='UPPER BB 30', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['sma_30'].plot(label='MIDDLE BB 30', linestyle='--',
                       linewidth=1.2, color='grey')
ETH_BTC['lower_bb1'].plot(label='LOWER BB 10', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['lower_bb'].plot(label='LOWER BB 20', linestyle='--',
                         linewidth=1, color='black')
ETH_BTC['lower_bb3'].plot(label='LOWER BB 30', linestyle='--',
                          linewidth=1, color='black')
plt.legend(loc='upper left')
plt.title('ETH_BTC BOLLINGER BANDS')
plt.show()


def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0

    for i in range(len(data)):
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, sell_price, bb_signal


def implement_bb2_strategy(data, lower_bb1, upper_bb1, lower_bb, upper_bb, lower_bb2, upper_bb2):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0

    for i in range(len(data)):
        if data[i-1] > lower_bb1[i-1] and data[i] < lower_bb1[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            if signal != 2:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 2
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        if data[i-1] > lower_bb2[i-1] and data[i] < lower_bb2[i]:
            if signal != 3:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 3
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)

        elif data[i-1] < upper_bb1[i-1] and data[i] > upper_bb1[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            if signal != -2:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -2
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb2[i-1] and data[i] > upper_bb2[i]:
            if signal != -3:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -3
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
    return buy_price, sell_price, bb_signal


buy_price, sell_price, bb_signal = implement_bb_strategy(
    ETH_BTC['Close'], ETH_BTC['lower_bb'], ETH_BTC['upper_bb'])
buy_price2, sell_price2, bb_signal2 = implement_bb2_strategy(
    ETH_BTC['Close'], ETH_BTC['lower_bb1'], ETH_BTC['upper_bb1'], ETH_BTC['lower_bb'], ETH_BTC['upper_bb'], ETH_BTC['lower_bb3'], ETH_BTC['upper_bb3'])


ETH_BTC['Close'].plot(label='CLOSE PRICES', alpha=0.3)
ETH_BTC['upper_bb1'].plot(label='UPPER BB 10', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['upper_bb'].plot(label='UPPER BB 20', linestyle='--',
                         linewidth=1, color='black')
ETH_BTC['upper_bb3'].plot(label='UPPER BB 30', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['sma_30'].plot(label='MIDDLE BB 30', linestyle='--',
                       linewidth=1.2, color='grey')
ETH_BTC['lower_bb1'].plot(label='LOWER BB 10', linestyle='--',
                          linewidth=1, color='black')
ETH_BTC['lower_bb'].plot(label='LOWER BB 20', linestyle='--',
                         linewidth=1, color='black')
ETH_BTC['lower_bb3'].plot(label='LOWER BB 30', linestyle='--',
                          linewidth=1, color='black')
plt.scatter(ETH_BTC.index, buy_price, marker='^',
            color='green', label='BUY', s=200)
plt.scatter(ETH_BTC.index, sell_price, marker='v',
            color='red', label='SELL', s=200)
plt.title('ETH_BTC BB STRATEGY TRADING SIGNALS')
plt.legend(loc='upper left')
plt.show()

position1 = []
position2 = []


def position_1():
    for i in range(len(bb_signal)):
        if bb_signal[i] > 1:
            position1.append(0)
        else:
            position1.append(1)

    for i in range(len(ETH_BTC['Close'])):
        if bb_signal[i] == 1:
            position1[i] = 1
        elif bb_signal[i] == -1:
            position1[i] = 0
        else:
            position1[i] = position1[i-1]


def position_2():
    for i in range(len(bb_signal2)):
        if bb_signal2[i] == 3 or bb_signal2[i] == 2 or bb_signal2[i] == 1 or bb_signal2[i] == -3 or bb_signal2[i] == -2 or bb_signal2[i] == -1:
            position2.append(bb_signal2[i])
        else:
            position2.append(0)

    for i in range(len(ETH_BTC['Close'])):
        if bb_signal2[i] == 1:
            position2[i] = 1
        elif bb_signal2[i] == 2:
            position2[i] = 2
        elif bb_signal2[i] == 3:
            position2[i] = 3
        elif bb_signal2[i] == -1:
            position2[i] = 0
        elif bb_signal2[i] == -2:
            position2[i] = -1
        elif bb_signal2[i] == -3:
            position2[i] = -2
        else:
            position2[i] = position2[i-1]


position_1()
position_2()


upper_bb = ETH_BTC['upper_bb']
lower_bb = ETH_BTC['lower_bb']
close_price = ETH_BTC['Close']
bb_signal = pd.DataFrame(bb_signal).rename(
    columns={0: 'bb_signal'}).set_index(ETH_BTC.index)
position = pd.DataFrame(position1).rename(
    columns={0: 'bb_position'}).set_index(ETH_BTC.index)

frames = [close_price, upper_bb, lower_bb, bb_signal, position]
strategy = pd.concat(frames, join='inner', axis=1)
strategy = strategy.reset_index().drop('Date', axis=1)

print(strategy.tail(7))


upper_bb1 = ETH_BTC['upper_bb1']
lower_bb1 = ETH_BTC['lower_bb1']
upper_bb = ETH_BTC['upper_bb']
lower_bb = ETH_BTC['lower_bb']
upper_bb2 = ETH_BTC['upper_bb3']
lower_bb2 = ETH_BTC['lower_bb3']
close_price = ETH_BTC['Close']
print(len(bb_signal2), len(ETH_BTC.index))
bb_signal2 = pd.DataFrame(bb_signal2).rename(
    columns={0: 'bb_signal2'}).set_index(ETH_BTC.index)
position2 = pd.DataFrame(position2).rename(
    columns={0: 'bb_position2'}).set_index(ETH_BTC.index)

frames2 = [close_price, upper_bb1, lower_bb1, upper_bb,
           lower_bb, upper_bb2, lower_bb2, bb_signal2, position2]
strategy2 = pd.concat(frames2, join='inner', axis=1)
strategy2 = strategy2.reset_index().drop('Date', axis=1)
print(strategy2.tail(7))

ETH_BTC_ret = pd.DataFrame(
    np.diff(ETH_BTC['Close'])).rename(columns={0: 'returns'})
bb_strategy_ret = []

for i in range(len(ETH_BTC_ret)):
    try:
        returns = ETH_BTC_ret['returns'][i]*strategy['bb_position'][i]
        bb_strategy_ret.append(returns)
    except:
        pass

bb_strategy_ret_df = pd.DataFrame(
    bb_strategy_ret).rename(columns={0: 'bb_returns'})

investment_value = 100000
number_of_stocks = math.floor(investment_value/ETH_BTC['Close'][-1])
bb_investment_ret = []

for i in range(len(bb_strategy_ret_df['bb_returns'])):
    returns = number_of_stocks*bb_strategy_ret_df['bb_returns'][i]
    bb_investment_ret.append(returns)

bb_investment_ret_df = pd.DataFrame(bb_investment_ret).rename(
    columns={0: 'investment_returns'})
total_investment_ret = round(
    sum(bb_investment_ret_df['investment_returns']), 2)
profit_percentage = math.floor((total_investment_ret/investment_value)*100)
print(cl('Profit gained from the BB strategy by investing $100k in ETH_BTC : {}'.format(
    total_investment_ret), attrs=['bold']))
print(cl('Profit percentage of the BB strategy : {}%'.format(
    profit_percentage), attrs=['bold']))


# def get_benchmark(stock_prices, start_date, investment_value):
#     spy = get_historic_data('SPY')
#     spy = spy.set_index('date')
#     spy = spy[spy.index >= start_date]['Close']
#     benchmark = pd.DataFrame(np.diff(spy)).rename(
#         columns={0: 'benchmark_returns'})

#     investment_value = investment_value
#     number_of_stocks = math.floor(investment_value/stock_prices[-1])
#     benchmark_investment_ret = []

#     for i in range(len(benchmark['benchmark_returns'])):
#         returns = number_of_stocks*benchmark['benchmark_returns'][i]
#         benchmark_investment_ret.append(returns)

#     benchmark_investment_ret_df = pd.DataFrame(
#         benchmark_investment_ret).rename(columns={0: 'investment_returns'})
#     return benchmark_investment_ret_df


# benchmark = get_benchmark(ETH_BTC['close'], '2020-01-01', 100000)

# investment_value = 100000
# total_benchmark_investment_ret = round(sum(benchmark['investment_returns']), 2)
# benchmark_profit_percentage = math.floor(
#     (total_benchmark_investment_ret/investment_value)*100)
# print(cl('Benchmark profit by investing $100k : {}'.format(
#     total_benchmark_investment_ret), attrs=['bold']))
# print(cl('Benchmark Profit percentage : {}%'.format(
#     benchmark_profit_percentage), attrs=['bold']))
# print(cl('BB Strategy profit is {}% higher than the Benchmark Profit'.format(
#     profit_percentage - benchmark_profit_percentage), attrs=['bold']))
