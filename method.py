from binance import Client
import pandas as pd 
import ccxt
import csv
import requests
from json import dumps
api_key = 'dECtCZJPAdCzILs3lgClUZoyEDsR3QfYBGcbMsVstwnHv1ttQAeabFN1x7D52fQr'
scert = 'L1KaBKKz2sEOI7cTMB2jvA4YiFJw6I68hEXbFG42ruOCaMkeMj9x6kcgJrdpIQvO'
client = Client(api_key, scert)

exg = ccxt.binance({
    'api_key': api_key,
    'secret': scert,
    'enableRateLimit': True,
    'adjustForTimeDifference': True,
    'createOrder': True,
    'options': {
      'defultType': 'spot'
    }
  })
def opened_order():
 
   
    order = []
    for x in client.get_open_orders():
        order.append(x)
    open_order = pd.DataFrame(order)
    open_order = open_order.iloc[:, [ 0, 4, 5]]
    open_order.index += 1
    open_order.price = open_order.price.astype(float)
    open_order.origQty = open_order.origQty.astype(float)

    return open_order


def get_ohlc(symbol,timeframe):

    boker = ccxt.binance()
    df = boker.fetch_ohlcv(symbol, timeframe, limit=500)
    frame = pd.DataFrame(df, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    frame=frame.astype(float)
    return frame

def write_to_csv(data,path):
  with open(path, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)
    print(f"Added {data[0]} to CSV file \U0001F4C4")

def get_usdt_amount():


  amount = exg.fetch_balance()['USDT']['free']
  return round(amount,2)

def get_amount(symbol):


  amount = exg.fetch_balance()[symbol.replace("USDT","")]['free']
  return round(amount,6)

def get_price(symbol):
  boker = ccxt.binance()
  df = boker.fetch_ohlcv(symbol, '1h', limit=10)
  df = pd.DataFrame(df, columns=['t', 'open', 'high', 'low', 'close', 'V'])
  close = df['close'].iloc[-1]

  return close

def post(urlserver,symbol,highest,lowest,amount):

    data_serv = {
            "symbol": symbol,  # Use variables directly for values
            "highest": highest,
            "lowest": lowest,
            "amount": amount,
        }

    try:
        json_data = dumps(data_serv)  # Directly serialize the list of dictionaries
        post = requests.post(url=urlserver, data=json_data, headers={"Content-Type": "application/json"})
        # get=requests.get(url=urlserver,data="hi")
        post.raise_for_status()  # Raise an exception for non-2xx status codes
        print("Request successful:", post.text)
    except requests.exceptions.RequestException as e:
        print("Error sending request:", e)