from flask import Flask, render_template,url_for,jsonify,Response, request
import pandas as pd 
from json import loads, dumps
import method
from threading import Thread
import time
from binance import Client
import ccxt
import csv 
import requests

app = Flask(__name__, template_folder='index') 
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
def get_usdt_amount():


  amount = exg.fetch_balance()['USDT']['free']
  return round(amount,2)

usdt=get_usdt_amount()
@app.route('/')
def home():


  return render_template('home.html',usdt=usdt)

@app.route('/get_table_data')
def get_table_data():
      try:
        df = method.opened_order()
        result = df.to_json(orient="table")
        parsed = loads(result)
        # print(dumps(parsed))
        json_object = loads(dumps(parsed))
        
        return jsonify(json_object['data'])  # Convert data to JSON format 
      except:
         return jsonify([{'symbol':'',
                          'price':'',
                          'origQty':''}])
@app.route("/saved", methods=['POST'])


def save_data():
  """Handles form submission and saves data to CSV."""
  if request.method == 'POST':

    symbol = request.form.get('symbol')
    highest = request.form.get('Highest')
    lowest = request.form.get('Lowest')
    amount = request.form.get('Amount')
    triger=request.form.get('Trigger')
    invest = request.form.get('total') 
    
    # print([invest,symbol,highest,lowest,amount,triger])
    amouex=round(float(float(amount)/float(lowest)),6)
    url="https://51cbfb8b-f881-46da-b3d5-c08b03e5d8c6-00-lo30suks4v4w.pike.replit.dev/webhook"
    if invest == None or invest =="off":
      
      order=exg.create_limit_buy_order(symbol=symbol,amount=float(float(amount) / float(lowest)),price=float(lowest))
      print(order)
      method.write_to_csv([symbol,lowest,highest,amouex],"position.csv")
      method.post(urlserver=url,symbol=symbol,highest=float(highest),lowest=float(lowest),amount=float(amouex))
      return 'sucess' ,200
      
    
    elif invest =="on":
      order=exg.create_limit_buy_order(symbol=symbol,amount=float(get_usdt_amount()*0.995/float(lowest)),price=float(lowest))
      print(order)
      method.write_to_csv([symbol,lowest,highest,amouex],"position.csv")
      method.post(urlserver=url,symbol=symbol,highest=float(highest),lowest=float(lowest),amount=float(amouex))

      return 'sucess' ,200
    
  else:
    return render_template('home.html',usdt=usdt)
  

      

if __name__ == "__main__":
  
  app.run(host='0.0.0.0',debug=True ,port=80)

