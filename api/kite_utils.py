import logging
from kiteconnect import KiteConnect
import os
from .utils import get_stock_data
import environ
from django.core.cache import cache
env = environ.Env()
environ.Env.read_env()  


def is_token_valid(access_token, request):
    try:
        session_key = request.session.session_key
        cache_key = f'api_creds_{session_key}'
        user_creds = cache.get(cache_key)
        if not user_creds:
            return False, 'User creds not present in cache'
    
        api_key = user_creds.get('api_key')

        
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)
    
    
        # Try a lightweight call; profile() is a good candidate.
        profile = kite.profile()
        return True, profile
    except Exception as e:
        # If there's an error (e.g., token expired or invalid), return False.
        print('Error occured while validating token', str(e))
        return False, str(e)
    
def generate_access_token(request_token, request):

    try:
        session_key = request.session.session_key
        cache_key = f'api_creds_{session_key}'
        user_creds = cache.get(cache_key)

        if not user_creds:
            print('API credentials not found or expired')
            return None

        api_key = user_creds.get('api_key')
        api_secret = user_creds.get('api_secret')

        kite = KiteConnect(api_key=api_key)
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        
        return access_token
        
    except Exception as e:
        print('Error occured while generating access token', e)
        return None


def generate_and_save_access_token(request_token):

    try:
        
        api_key = env("KITE_API_KEY")
        api_secret = env("KITE_API_SECRET")
        access_token_file = "access_token.txt"

        if os.path.exists(access_token_file):
            print('As access token already exists in fs, reading it as is')
            with open(access_token_file, "r") as f:
                access_token = f.read().strip()
                return

        kite = KiteConnect(api_key=api_key)
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
 
        # Save token for reuse during the same day
        with open(access_token_file, "w") as f:
            f.write(access_token)
            return
        
    except Exception as e:
        print('Error occured while generating access token', e)
        return

  
def get_kite_client(access_token):
    api_key = env("KITE_API_KEY")
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite


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


def get_zerodha_holdings(access_token):
    '''
    Returns zerodha holdings as list of objects with each object representing a positions in current stock
    '''
    data = []
    kite = get_kite_client(access_token)
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
   


