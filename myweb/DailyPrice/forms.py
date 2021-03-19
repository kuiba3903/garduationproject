from DailyPrice.models import DailyPrice_DP,DailyPrice_BP
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class searchForm(forms.ModelForm):
    market_name_items = DailyPrice_BP.objects.all().distinct().values_list("market_index", "market_name")
    market_name = forms.ChoiceField(label="批发市场",choices=market_name_items, widget=forms.Select(attrs={'class': "form-control-nowidth"}))

    class Meta:
        model = DailyPrice_DP
        fields = ["market_name"]
