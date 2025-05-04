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



class StoreAPICredsView(APIView):
  def post(self, request):
    try:
        data = json.loads(request.body)
        user_api_key = data.get('api_key')
        user_api_secret = data.get('api_secret')
        
        if not user_api_key or not user_api_secret:
            return Response({'error': 'Missing credentials'}, status=400)
        
        # Use a unique key tied to the user/session (assuming session management)
        # For example, using the session key:
        session_key = request.session.session_key or request.session.create()
        cache_key = f'api_creds_{session_key}'
        
        # Store in cache for 5 minutes (300 seconds)
        cache.set(cache_key, {'api_key': user_api_key, 'api_secret': user_api_secret}, timeout=300)
        
        return Response({'message': 'Credentials stored successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)




class AuthCheckAPIView(APIView):
  

  def get(self,request):
    try:
      access_token = request.COOKIES.get("access_token")

      if not access_token:
        return Response({"authenticated": False, "error": "No access token found"}, status=401)
      valid, result = is_token_valid(access_token, request)

      if valid:
          return Response({"authenticated": True, "profile": result})
      else:
          return Response({"authenticated": False, "error": result}, status=401)

    except Exception as e:
      return Response({"authenticated": False,"error": f'Error occured while checking authentication : {e}'})


class LogoutAPIView(APIView):
  

  def post(self,request):
    try:
      
      access_token = request.COOKIES.get("access_token")

      if not access_token:
        return Response({"error": "You are not logged in"}, status=401)

      response = Response({"message": "Logged out"})
      response.delete_cookie('access_token')
      return response

    except Exception as e:
      return Response({'error': f'Error occured while logging out : {e}'}, status=401)



class LoginAPIView(APIView):
  

  def get(self,request):
    try:
      status = request.GET.get("status")
      request_token = request.GET.get("request_token")

      if not status or not request_token:
        return Response({'error': 'Either status or request token missing from query params'})
      
      if status != 'success':
        return Response({'error': f'Status is not success'})


      #generate and send access token back as cookie
      access_token = generate_access_token(request_token, request)

      if not access_token:
        return Response({"error": "Access token generation failed"})

      print('Access token generated successfully')
      
      react_app_url = env("REACT_FRONTEND_URL")+'/portfolio'
      
      
      response = redirect(react_app_url)
      response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=86400,      # 1 day in seconds
        httponly=True,      # Helps prevent XSS attacks
        secure=False,        # Use only with HTTPS
        #samesite='Lax'      # Adjust based on your requirements (Lax, Strict, None)
      )
      return response
   
    except Exception as e:
      return Response({'error': f'Error occured while authentication : {e}'})


