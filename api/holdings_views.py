from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
import yfinance as yf
from .utils import get_stock_data, get_stocks_data, get_stock_hist_data, get_stocks_hist_data
from django.core.cache import cache
import json

from .kite_utils import get_zerodha_holdings, get_zerodha_holding, generate_access_token, is_token_valid
from .models import WishList
from django.shortcuts import get_object_or_404
from rest_framework import status
import environ
env = environ.Env()
environ.Env.read_env()  


#stock holding views
class StockHoldingAPIView(APIView):
  def get(self, request):
    
    try:

      tickers = request.GET.get("tickers")
      data = get_zerodha_holding(tickers)
      if data:
        return Response(data)
      
      return Response({"error": "Not enough data"}, status=400)
    
    except Exception as e:
      return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
    

class StocksHoldingsAPIView(APIView):
  def get(self, request):
    
    try:
      access_token = request.COOKIES.get("access_token")

      if not access_token:
        return Response({'error':'Unauthorized', 'data':[]}, status=401)
      
      data = get_zerodha_holdings(access_token)
      if data:
        return Response({'status':'success', 'data':data})
      
      return Response({"error": "Not enough data", 'data':[]}, status=400)
    
    except Exception as e:
      return Response({'error': f'{e}', 'data' : []}, status=status.HTTP_400_BAD_REQUEST)
  

#stock price history views
class StockPriceHistoryAPIView(APIView):
  def get(self, request):
    ticker = request.GET.get("ticker")
    timeframe = request.GET.get("time")

    data = get_stock_hist_data(ticker, timeframe)


    if data:
      return Response(data)
    
    return Response({"error": "Not enough historical data"}, status=400)

class StocksPricesHistoryAPIView(APIView):
  def get(self, request):
    tickers = request.GET.get("tickers")

    if not tickers:
      return Response({"error": "No tickers provided"}, status=400)
    
    tickers_list = tickers.split(',')
    data = get_stocks_hist_data(tickers_list)
    if data:
      return Response(data)
    
    return Response({"error": "Not enough data"}, status=400)
    
#stock price views

class StockPriceAPIView(APIView):
  def get(self, request):
    ticker = request.GET.get("ticker")
    data = get_stock_data(ticker)
    if data:
      return Response(data)
    
    return Response({"error": "Not enough data"}, status=400)
    


class StocksPricesAPIView(APIView):
  def get(self, request):
    tickers = request.GET.get("tickers")

    if not tickers:
      return Response({"error": "No tickers provided"}, status=400)
    
    tickers_list = tickers.split(',')
    data = get_stocks_data(tickers_list)
    if data:
      return Response(data)
    
    return Response({"error": "Not enough data"}, status=400)
    
