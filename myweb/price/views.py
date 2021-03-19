from django.shortcuts import render
from .forms.serachForm import searchForm
from django.http import JsonResponse, HttpResponse
from .models import Price
import json
from django.db.models import Q

# Create your views here.


def price(request):
    form = searchForm(initial={"province_name": "34", "vegetable_name": "13075"})
    return render(request, "price.html", {"forms": form})


def getVegetable(request):
    vegetable_index = request.GET.get("vegetable_name")
    vegetable_name = Price.objects.filter(vegetable_index=vegetable_index).distinct().values_list(
        "craft_index", "craft_name")
    # print(vegetable_name)
    data={}
    for i in vegetable_name:
        data[i[0]] = i[1]
    # print(data)
    # 字典转换为json格式
    return HttpResponse(json.dumps(data))

def getMarket(request):
    vegetable_index = request.POST.get("vegetable_name")
    craft_index = request.POST.get("craft_name")
    province_index = request.POST.get("province_name")
    market_name = Price.objects.filter(Q(vegetable_index=vegetable_index)
                                       & Q(craft_index=craft_index)
                                       & Q(province_index=province_index)).distinct().values_list(
        "market_index", "market_name")
    print(market_name)
    data = {}
    for i in market_name:
        data[i[0]] = i[1]
    # print(data)
    # 字典转换为json格式
    return HttpResponse(json.dumps(data))

def getOnlyMarket(request):
    province_index = request.POST.get("province_name")
    market_name = Price.objects.filter(Q(province_index=province_index)).distinct().values_list(
        "market_index", "market_name")
    print(market_name)
    data = {}
    for i in market_name:
        data[i[0]] = i[1]
    # print(data)
    # 字典转换为json格式
    return HttpResponse(json.dumps(data))

def search(request):
    # print(request.POST)
    vegetable_index = request.POST.get("vegetable_name")
    craft_index = request.POST.get("craft_name")
    province_index = request.POST.get("province_name")
    market_index = request.POST.get("market_name")
    data = Price.objects.filter(Q(vegetable_index=vegetable_index)
                                & Q(craft_index=craft_index)
                                & Q(province_index=province_index)
                                & Q(market_index=market_index)).distinct().values_list("price_2019", "price_2020")
    # print(data)
    if(not data):
        res = {"price_2019": None, "price_2020": None}
        return JsonResponse(res)
    res = {
        "price_2019": data[0][0],
        "price_2020": data[0][1]
    }
    # print(res)
    return JsonResponse(res)