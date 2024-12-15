import time
import pandas as pd
from binance.client import Client 
import csv
from datetime import datetime, timedelta
import os
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

api_key = ""
api_secret = ""

def calculate_A(balance3, n):
    # Calculate B
    B = balance3 / (2**(n + 1) - 1)
    
    # Calculate Ai for i = 0, 1, ..., n
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

crypto = TA_Handler(
    symbol="PEPEUSDT",
    exchange="binance",
    screener="Crypto",
    interval=Interval.INTERVAL_5_MINUTES,
    timeout=None
)

crypto_15 = TA_Handler(
    symbol="PEPEUSDT",
    exchange="binance",
    screener="Crypto",
    interval=Interval.INTERVAL_15_MINUTES,
    timeout=None
)

import requests

def get_binance_historical_data(symbol, interval, end_time, limit=1000):
    # Calculate the start time
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

@app.route("/")
def index():
    return "Flask app running on Render!"

# Main loop (can be adapted to your Flask route)
@app.route("/run")
def run_trading():
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

            time.sleep(5)

            chang = round(((float(candle['close']) - float(candle['open'])) / float(candle['open'])) * 100, 8)
            chang_15 = round(((float(candle_15['close']) - float(candle_15['open'])) / float(candle_15['open'])) * 100, 8)

            # Your trading logic goes here

        except Exception as e:
            print("An error occurred while fetching analysis:", e)
            message = False
            with open('log.txt', 'a') as f:
                try:
                    f.write(f"{formatted_date_time} _{e}\n")
                    f.write("\n")
                except:
                    print('error within error')
            time.sleep(60)
    
    return "Trading logic executed!"

# Get the port from environment or default to 8080
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
