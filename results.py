import time
import pandas as pd
import requests
from binance.client import Client
from tradingview_ta import TA_Handler, Interval, Exchange
import os
from datetime import datetime, timedelta

# Set up environment variables for sensitive information
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

def calculate_A(balance3, n):
    B = balance3 / (2**(n + 1) - 1)
    A = [int(B * 2**i) for i in range(n+1 )]
    return A

no_position3 = True
balance3 = 1200
n = 3
coins3 = 0
buy_price3 = 0
time_stor3 = 0
trade_loss3 = 0
trade_won3 = 0
total_invst = 0
buy1 = True
buy2 = False
buy3 = False
buy4 = False
inv1 = calculate_A(balance3, n)[0]
inv2 = calculate_A(balance3, n)[1]
inv3 = calculate_A(balance3, n)[2]
inv4 = calculate_A(balance3, n)[3]

# Trading View and Binance API setup
crypto = TA_Handler(
    symbol="PEPEUSDT",
    exchange="binance",
    screener="Crypto",
    interval=Interval.INTERVAL_5_MINUTES,
    timeout=None
)

def get_binance_historical_data(symbol, interval, end_time, limit=1000):
    start_time = end_time - timedelta(minutes=30)
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={int(start_time.timestamp())*1000}&endTime={int(end_time.timestamp())*1000}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    else:
        print("Error:", response.status_code)
        return None

def log_trade(message):
    """ Function to log trade activities, could be enhanced to save to database instead of file. """
    print(message)
    with open('trades_summary_PEPE3.txt', 'a') as f:
        f.write(f"{message}\n")
        
def buy_condition3(SMA10_):
    return chang <= -0.45

def sell_condition3(buy_price3, SMA10_, price, coins3, total_invst):
    return (price * coins3) > 1.01 * total_invst

message = True
while True:
    try:
        end_time = datetime.now()
        symbol = 'PEPEUSDT'  
        interval = '5m'     
        historical_data = get_binance_historical_data(symbol, interval, end_time)
        historical_data_15 = get_binance_historical_data(symbol, '15m', end_time)
        
        candle = historical_data.iloc[-2]
        candle_15 = historical_data_15.iloc[-2]

        SMA10 = crypto.get_analysis().indicators['SMA10']
        STOCH = crypto.get_analysis().indicators['Stoch.K']
        volumes = crypto.get_analysis().indicators['volume']
        
        bclient = Client(api_key, api_secret, testnet=False) 
        symbol_info = bclient.get_ticker(symbol="PEPEUSDT")
        price = float(symbol_info['askPrice'])

        current_time_epoch = int(time.time())
        formatted_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time_epoch))
        
        chang = round(((float(candle['close']) - float(candle['open'])) / float(candle['open'])) * 100, 8)
        chang_15 = round(((float(candle_15['close']) - float(candle_15['open'])) / float(candle_15['open'])) * 100, 8)

        time.sleep(5)  # Sleep between loops

        # Buying logic
        if no_position3 and buy_condition3(SMA10):
            print('Entry found.')
            buy_price3 = price
            inv1 = calculate_A(balance3, n)[0]
            total_invst = inv1
            coins3 = int((inv1 - inv1 * 0.001) / buy_price3)
            balance3 -= inv1
            log_trade(f"{formatted_date_time}: Buy condition met. Price: {price:.8f} STOCH: {STOCH:.2f} Chag: {chang:.2f} Amount: {balance3:.2f} Total_Invt: {total_invst:.2f}")
            no_position3 = False
            buy1 = False
            buy2 = True
        
        if sell_condition3(buy_price3, SMA10, price, coins3, total_invst) and chang_15 >= 0.8:
            print('Sold.')
            message = True
            sell_price3 = price
            balance3 += coins3 * 0.999 * price
            coins3 = 0
            no_position3 = True
            buy1 = True
            buy2 = False
            log_trade(f"{formatted_date_time}: Sell condition met. Price: {price:.8f} STOCH: {STOCH:.2f} Chag: {chang_15:.2f} Amount: {balance3:.2f} Total_Invt: {total_invst:.2f}")
            # Track win/loss logic
            if sell_price3 <= buy_price3:
                trade_loss3 += 1
            else:
                trade_won3 += 1

        if no_position3 and message:
            print("Waiting for entry...")

        time.sleep(60)  # Delay to avoid excessive API calls

    except Exception as e:
        print("An error occurred while fetching analysis:", e)
        message = False
        with open('log.txt', 'a') as f:
            try:
                f.write(f"{formatted_date_time} _{e}\n")
                f.write("\n")
            except:
                print('Error in error logging')
        time.sleep(60)
