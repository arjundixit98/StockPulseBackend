import logging
from kiteconnect import KiteConnect
import os
from .utils import get_stock_data
import environ
env = environ.Env()
environ.Env.read_env()  


def get_kite_client():


  api_key = env("KITE_API_KEY")
  api_secret = env("KITE_API_SECRET")
  access_token_file = "access_token.txt"
  print(api_key)

  kite = KiteConnect(api_key=api_key)

  # Load existing access token if available
  if os.path.exists(access_token_file):
      with open(access_token_file, "r") as f:
          access_token = f.read().strip()
          kite.set_access_token(access_token)
  else:
      # First-time login (manual step required)
      print(kite.login_url())
      request_token = input("Enter request token: ")
      data = kite.generate_session(request_token, api_secret=api_secret)
      access_token = data["access_token"]

      # Save token for reuse during the same day
      with open(access_token_file, "w") as f:
          f.write(access_token)

      kite.set_access_token(access_token)

  print(kite.holdings()[1])
  return kite


  # Now you can make API calls
  #print(kite.holdings()[0])

def getFromHoldingObject(holding, attribute):
    return holding.get(attribute)

def per_change(initial_value, current_value):
    if current_value == 0:
        return 0
    return round(((current_value-initial_value)/initial_value) * 100,2)

def get_zerodha_holding(tickers):
    data = []
    tickers = tickers.split(',')
    kite = get_kite_client()
    holdings = kite.holdings()
    
    for holding in holdings:
        if holding.get('tradingsymbol')+'.NS' in tickers:
            data.append(holding)

    return data


def get_zerodha_holdings():
    '''
    Returns zerodha holdings as list of objects with each object representing a positions in current stock
    '''
    data = []
    kite = get_kite_client()
    holdings = kite.holdings()
    
    for holding in holdings:
      ticker = holding.get('tradingsymbol')+'.NS'
      stock_data = get_stock_data(ticker)


      
      currentPrice = round(holding.get('last_price'),2)
      
      quantity = holding.get('quantity')
      current_value = currentPrice * quantity
      invested_value = holding.get('average_price') * quantity 
      pnl = current_value - invested_value
      percent_increase_by_value = per_change(invested_value, current_value)
      weekHigh52 =  stock_data.get('weekHigh52')
      weekLow52 = stock_data.get('weekLow52')
      percentFrom52WeekHigh = round(((weekHigh52 - currentPrice) / weekHigh52) * 100,2)
      percentFrom52WeekLow = round(((currentPrice - weekLow52) / weekLow52) * 100,2)
      data.append({
            'symbol': ticker,
            'name': stock_data.get('name') or ticker,
            'quantity': quantity,
            'avgPrice': round(holding.get('average_price'),2),
            'currentPrice': currentPrice,
            'investedValue': round(invested_value,2),
            'value': round(current_value,2),
            'pl': round(pnl,2),
            'plPercentage': percent_increase_by_value,
            'dayChange': round(holding.get('day_change_percentage'),2),
            'sector': stock_data.get('sector'),
            'pe': stock_data.get('pe'),
            'weekHigh52': weekHigh52,
            'weekLow52': weekLow52,
            'percentFrom52WeekHigh': percentFrom52WeekHigh,
            'percentFrom52WeekLow': percentFrom52WeekLow,
            'stock': stock_data

      })
      
    return data
   


