from django.urls import path
from . import wishlist_views, auth_views, holdings_views

urlpatterns = [
    
    #auth urls
    path('login',  auth_views.LoginAPIView.as_view(), name="login"),
    path('logout',  auth_views.LogoutAPIView.as_view(), name="logout"),
    path('auth-check',  auth_views.AuthCheckAPIView.as_view(), name="auth-check"),
    path('store-api-creds',  auth_views.StoreAPICredsView.as_view(), name="store-api-creds"),

    #stock price urls
    path('stock', holdings_views.StockPriceAPIView.as_view(),name="stock-price"),
    path('stocks', holdings_views.StocksPricesAPIView.as_view(),name="stocks-prices"),

    #stock history urls
    path('stock_hist', holdings_views.StockPriceHistoryAPIView.as_view(),name="stock-price-hist"),
    path('stocks_hist', holdings_views.StocksPricesHistoryAPIView.as_view(),name="stocks-prices-hist"),

    #wishlist urls
    path('wishlist', wishlist_views.WishListAPIView.as_view(), name="get-wishlist"),
    path('wishlist/<int:wishlistid>', wishlist_views.WishListAPIView.as_view(), name="delete-wishlist"),
    path('wishlists/', wishlist_views.AllWishListsAPIView.as_view(), name="get-wishlists"),

    #zerodha holdings urls
    path('holding', holdings_views.StockHoldingAPIView.as_view(), name="get-holding"),
    path('holdings', holdings_views.StocksHoldingsAPIView.as_view(), name="get-holdings"),        
]


