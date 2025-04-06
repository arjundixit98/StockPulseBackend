from django.urls import path 
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('wishlists/',views.wishlist_list, name='wishlist_list'),
    path('wishlists/create/', views.wishlist_create, name="wishlist_create"),
    path('wishlists/edit/<int:wishlist_id>/', views.wishlist_edit, name="wishlist_edit"),
    path('wishlists/delete/<int:wishlist_id>/', views.wishlist_delete, name='wishlist_delete'),
]
