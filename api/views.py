from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
import yfinance as yf
from .utils import get_stock_data, get_stocks_data, get_stock_hist_data, get_stocks_hist_data

from .kite_utils import get_zerodha_holdings, get_zerodha_holding
from .models import WishList
from django.shortcuts import get_object_or_404
from rest_framework import status



# class WishListAPIView(APIView):
#   def get(self, request, wishlistname):
#     try:
#       wishlist = WishList.objects.get(wishlistname=wishlistname)
#       if wishlist:
#         return Response({"tickers":wishlist.tickers})
      
#     except Exception as e:
#       return Response({"error": "Wishlist notfound"}, status=400)



# class AllWishListsAPIView(APIView):
#   def get(self, request):
#     data = []
#     wishlists = WishList.objects.all().order_by('-created_at')
#     for wishlist in wishlists:
#       data.append({"wishlistname":wishlist.wishlistname,
#                    "tickers":wishlist.tickers})
    
#     if data:
#       return Response(data)
    
#     return Response({"error": "No wishlists found"}, status=400)


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
      
      data = get_zerodha_holdings()
      if data:
        return Response(data)
      
      return Response({"error": "Not enough data"}, status=400)
    
    except Exception as e:
      return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
    
    

class WishListCreateAPIView(APIView):
  def post(self, request):
    print(request.body)


class WishListAPIView(APIView):
  def put(self, request):
    try:
      wishlistname = request.GET.get("name")
      wishlist = WishList.objects.get(name=wishlistname)
      if not wishlist:
        return Response({"error": f"Wishlist not found, {e}"}, status=400)
      
      wishlist.tickers.extend(request.data)
      wishlist.save()
      
      return Response({'message': 'Wishlist updated successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      return Response({"error": f"Wishlist not found, {e}"}, status=400)

  def post(self, request):
    '''
    Stores the payload received and creates a new wishlist
    '''
    try:
      data = request.data
      print(data)
      wishlist = WishList(name=data.get('name'),tickers=data.get('symbols'))
      wishlist.save()
      

      return Response({'message': 'Wishlist saved successfully'}, status=status.HTTP_201_CREATED)
    
            
    except Exception as e:
      return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request, wishlistid):
    '''
    Deletes the wishlist using wishlist id
    '''
    try:
      data = request.data
      print(data)
      wishlist = WishList.objects.get(pk=wishlistid)
      wishlist.delete()
      

      return Response({'message': 'Wishlist successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    
            
    except Exception as e:
      return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    
  def get(self, request):
    '''
    Input : Give wishlist name as query param -> /wishlist?name=wishlistname
    Returns : A list of tickers inside the wishlist 
    '''
   
    try:

      wishlistname = request.GET.get("name")
      wishlist = WishList.objects.get(name=wishlistname)
      if wishlist:
        return Response(wishlist.tickers)
      
    except Exception as e:
      return Response({"error": f"Wishlist not found, {e}"}, status=400)



class AllWishListsAPIView(APIView):
  '''
  Input : Given URL is entered as -> /wishlists
  Returns : A list of objects each containing name and tickers sorted by created time
  '''
  def get(self, request):
    try:
      data = []
      wishlists = WishList.objects.all().order_by('-created_at')
      for wishlist in wishlists:
        data.append({"id":wishlist.id, "name":wishlist.name, "symbols":wishlist.tickers})
      
     
      return Response(data)
      
    except Exception as e:
      return Response({"error": f"Error occured, e"}, status=400)



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
    
