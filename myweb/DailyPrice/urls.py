from django.contrib import admin
from django.urls import path
from .views import market_brief,fenlei,news_process,search_2011_2020,image,query_datePrice,query_marketData,market_show, predict_arima
urlpatterns = [
    path('market_brief/<int:market_index>', market_brief, name="market_brief"),
    path('query_datePrice/', query_datePrice, name="query_datePrice"),
    path('query_marketData/', query_marketData, name="query_marketData"),
    path('market_show/', market_show, name="market_show"),
    path('image/', image, name="image"),
    path("news/" ,news_process,name="news_process"),
    path("fenlei/" ,fenlei,name="fenlei"),
    path("predict_arma/",predict_arima,name="predict_arima"),
    path("search_2011_2020/",search_2011_2020,name="search_2011_2020")
]