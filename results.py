import time
import pandas as pd
from binance.client import Client 
import csv
from datetime import datetime, timedelta
import os
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta



api_key=""
api_secret=""


def calculate_A(balance3, n):
    # Calculate B
    B = balance3 / (2**(n + 1) - 1)
    
    # Calculate Ai for i = 0, 1, ..., n
    A = [int(B * 2**i) for i in range(n+1 )]
    
    return A

no_position3 = True
balance3=1200
n=3
coins3=0
buy_price3=0
time_stor3=0
trade_loss3=0
trade_won3=0
total_invst=0
buy1=True
buy2=False
buy3 = False
buy4 = False
inv1=calculate_A(balance3, n)[0]
inv2=calculate_A(balance3, n)[1]
inv3=calculate_A(balance3, n)[2]
inv4=calculate_A(balance3, n)[3]



crypto = TA_Handler(
    symbol="PEPEUSDT",
    exchange="binance",
    screener="Crypto",
    interval=Interval.INTERVAL_5_MINUTES,
    timeout=None
)
crypto_15=TA_Handler(
    symbol="PEPEUSDT",
    exchange="binance",
    screener="Crypto",
    interval=Interval.INTERVAL_15_MINUTES,
    timeout=None
)


import requests




# Example usage







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
        return df  # Return the row before the last
    else:
        print("Error:", response.status_code)
        return None

# Get the current time







message =True
while True:
    try:
    
        

        
        end_time = datetime.now()

# Example usage
        symbol = 'PEPEUSDT'  # Symbol of the trading pair (e.g., BTCUSDT for Bitcoin/USDT)
        interval = '5m'     # Interval of the candlesticks (e.g., '1m' for 1 minute, '1h' for 1 hour)
        historical_data=get_binance_historical_data(symbol, interval, end_time)
        historical_data_15=get_binance_historical_data(symbol, '15m', end_time )
        
        candle = historical_data.iloc[-2]
        candle_15 = historical_data_15.iloc[-2]
        

        # pre_candle = float(historical_data.iloc[-3]['close'])
        # last_candle = float(historical_data.iloc[-2]['close'])

        
        
        
        SMA10= crypto.get_analysis().indicators['SMA10']
        
        STOCH= crypto.get_analysis().indicators['Stoch.K']

        volumes=crypto.get_analysis().indicators['volume']
        
        
        bclient = Client(api_key, api_secret, testnet=False) 
        symbol_info = bclient.get_ticker(symbol="PEPEUSDT")

        price= float(symbol_info['askPrice'])

        current_time_epoch = int(time.time())
        # time_current_local = datetime.datetime.now()
        
        
        # Convert timestamp to datetime object with UTC timezone
        date_time = time.ctime(current_time_epoch)
        
        # time_current = int(time.time()) * 1000

    # Convert Unix timestamp to datetime
        
        
    # Format the datetime object as a string

        # date_time+= timedelta(hours=1)
    # Format the datetime object as a string
        formatted_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time_epoch))
        
        

# Assuming time_current is a timestamp in milliseconds
        
            

        time.sleep(5) 

        
        # pre_candle = latest_data.iloc[-2]
        # Print out open and close prices
        
        
        chang= round(((float(candle['close']) - float(candle['open'])) / float(candle['open'])) * 100, 8)
        chang_15= round(((float(candle_15['close']) - float(candle_15['open'])) / float(candle_15['open'])) * 100, 8)


        # Calculate percentage price change for the last 5 minutes
        
        
        #time.sleep(100)
        
                        

            
        def buy_condition3(SMA10_):
                    #  818        811         811           816 
            return  chang  <= -.45

        #def sell_condition(buy_price, current_price):
            #return (current_price - buy_price) / buy_price >= 0.01 or (current_price - buy_price) / buy_price <= -0.01
        def sell_condition3(buy_price3, SMA10_,price,coins3,total_invst):
            return  (price *coins3) > 1.01* total_invst # or  price *coins3 <= total_invst/1.03
        

        
        
        
        if no_position3:
            

            if buy_condition3(SMA10) and buy1 ==True:
                print('Entry found.')
                buy_price3=price
                
                inv1=calculate_A(balance3, n)[0]
                inv2=calculate_A(balance3, n)[1]
                inv3=calculate_A(balance3, n)[2]

                total_invst = inv1

                
                coins3= int((inv1-inv1*0.001)/buy_price3 )
                balance3 -= inv1
                
                
                with open('trades_summary_PEPE3.txt', 'a') as f:
                        f.write(f"{formatted_date_time}: Buy condition met.\n")
                        f.write(f"{formatted_date_time}: Price: {price:.8f}  STOCH:  {STOCH:.2f}   Chag: {chang:.2f}    Amount: {balance3:.2f} Total_Invt: {total_invst:.2f} \n")
                        f.write("\n")
                        
                buy2 = True
                buy1 = False
                no_position3 = False
                
        if buy_price3*0.98>=price and buy2 ==True and chang  <= -.45:
            
            buy_price3=price
            
            print('2nd entry found.')

            coins3+= int((inv2-inv2*0.001)/buy_price3 )
            total_invst += inv2
            buy3 = True
            balance3 -= inv2
            
            
            with open('trades_summary_PEPE3.txt', 'a') as f:
                    f.write(f"{formatted_date_time}: Buy condition met***Adding position***.\n")
                    f.write(f"{formatted_date_time}: Price: {price:.8f}  STOCH:  {STOCH:.2f}   Chag: {chang:.2f}    Amount: {balance3:.2f} Total_Invt: {total_invst:.2f} \n")
                    f.write("\n")
                    
            
            no_position3 = False
            buy2 = False

        if buy_price3*0.97>=price and buy3 ==True and chang  <= -.45:
            
            buy_price3=price
            print('3th entry found.')
            
            coins3+= int((inv3-inv3*0.001)/buy_price3 )
            total_invst += inv3
            balance3 -= inv3
            
            with open('trades_summary_PEPE3.txt', 'a') as f:
                    f.write(f"{formatted_date_time}: Buy condition met***Adding position***.\n")
                    f.write(f"{formatted_date_time}: Price: {price:.8f}  STOCH:  {STOCH:.2f}   Chag: {chang:.2f}    Amount: {balance3:.2f} Total_Invt: {total_invst:.2f} \n")
                    f.write("\n")
                    
            
            
            buy4 = True
            buy3 = False

        if buy_price3*0.95>=price and buy4 ==True and chang  <= -.45:
            
            buy_price3=price
            print('4th entry found.')
            
            coins3+= int((inv4-inv4*0.001)/buy_price3 )
            total_invst += inv4
            balance3 -= inv4
            
            with open('trades_summary_PEPE3.txt', 'a') as f:
                    f.write(f"{formatted_date_time}: Buy condition met***Adding position***.\n")
                    f.write(f"{formatted_date_time}: Price: {price:.8f}  STOCH:  {STOCH:.2f}   Chag: {chang:.2f}    Amount: {balance3:.2f} Total_Invt: {total_invst:.2f} \n")
                    f.write("\n")
                    
            
            
            
            buy4 = False

        
        if no_position3 ==False:

            if sell_condition3(buy_price3, SMA10,price,coins3,total_invst) and chang_15 >= 0.8:
                # Execute sell order
                print('Sold.')
                message=True
                sell_price3 = price
                balance3 += coins3*0.999*price
                
                coins3 = 0
                no_position3 =True

                # Your sell logic here
                buy1 = True
                buy2 = False
                time.sleep(55*5)

                
                

                if sell_price3 <= buy_price3:
                    trade_loss3+=1
                    total_trades3=trade_loss3 + trade_won3

                    with open('trades_summary_PEPE3.txt', 'a') as f:
                        f.write(f"{formatted_date_time} _____TRADE LOSS_____. Total Trades: {total_trades3}\n")
                else:
                    trade_won3+=1
                    total_trades3=trade_loss3 + trade_won3
                    with open('trades_summary_PEPE3.txt', 'a') as f:
                        f.write(f"{formatted_date_time} _____TRADE WON_____. Total Trades: {total_trades3}\n")

                with open('trades_summary_PEPE3.txt', 'a') as f:
                        f.write(f"{formatted_date_time}: Sell condition met.\n")
                        f.write(f"{formatted_date_time}: Price: {price:.8f}  STOCH:  {STOCH:.2f}   Chag: {chang_15:.2f}    Amount: {balance3:.2f} Total_Invt: {total_invst:.2f} \n")
                        f.write("\n")









        if no_position3 & message:
             print("waiting entry...")
             message = False



    except Exception as e:
        print("An error occurred while fetching analysis:", e)
        message = False
        with open('log.txt', 'a') as f:
            try:
                f.write(f"{formatted_date_time} _{   e}\n")
                
                f.write("\n")
            except:
                print('error within error')

        time.sleep(60)

    
            
    
        

