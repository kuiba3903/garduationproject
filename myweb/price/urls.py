"""app price的路由分配"""
from django.contrib import admin
from django.urls import path
from .views import price, getOnlyMarket,getVegetable, getMarket, search
urlpatterns = [
    path('price/price/', price, name="price"),
    path('getVegetable/', getVegetable, name="getVegetable"),
    path('getMarket/', getMarket, name="getMarket"),
    path('search/', search, name="search"),
    path('getOnlyMarket/', getOnlyMarket, name="getOnlyMarket")
]