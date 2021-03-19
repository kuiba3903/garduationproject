"""蔬菜类型、省、批发市场查询下拉框"""

from price.models import Price
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class searchForm(forms.ModelForm):
    province_name_items = Price.objects.all().distinct().values_list("province_index", "province_name")
    # province_name_items.append(("null", "--请选择--"))
    # print(province_name_items)
    province_name = forms.ChoiceField(label="省份", choices=province_name_items, widget=forms.Select(attrs={'class': "form-control-nowidth"}))

    vegetable_name_items = Price.objects.all().distinct().values_list("vegetable_index", "vegetable_name")
    vegetable_name = forms.ChoiceField(label="类型", choices=vegetable_name_items,widget=forms.Select(attrs={'class': "form-control-nowidth"}))

    craft_name_items = Price.objects.filter(vegetable_index=13075).distinct().values_list("craft_index", "craft_name")
    craft_name = forms.ChoiceField(label="名称", choices=craft_name_items, widget=forms.Select(attrs={'class': "form-control-nowidth"}))

    market_name_items = Price.objects.filter(province_index=34).distinct().values_list("market_index", "market_name")
    print(market_name_items)
    market_name = forms.ChoiceField(label="市场", choices=market_name_items, widget=forms.Select(attrs={'class': "form-control-nowidth"}))

    class Meta:
        model = Price
        fields = ["vegetable_name", "craft_name", "province_name", "market_name"]
