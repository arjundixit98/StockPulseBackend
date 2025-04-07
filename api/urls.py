from django.urls import path
from . import views

urlpatterns = [
    
    path('stock_hist', views.StockPriceHistoryAPIView.as_view(),name="stock-price-hist"),
    path('stock', views.StockPriceAPIView.as_view(),name="stock-price"),
    path('stocks', views.StocksPricesAPIView.as_view(),name="stocks-prices"),
    path('stocks_hist', views.StocksPricesHistoryAPIView.as_view(),name="stocks-prices-hist"),
    
    path('wishlist', views.WishListAPIView.as_view(), name="get-wishlist"),
    path('wishlist/<int:wishlistid>', views.WishListAPIView.as_view(), name="delete-wishlist"),
    path('wishlists', views.AllWishListsAPIView.as_view(), name="get-wishlists"),
    path('holding', views.StockHoldingAPIView.as_view(), name="get-holding"),
    path('holdings', views.StocksHoldingsAPIView.as_view(), name="get-holdings"),
    path('login',  views.LoginAPIView.as_view(), name="login"),
    path('auth-check',  views.AuthCheckAPIView.as_view(), name="auth-check")
]


