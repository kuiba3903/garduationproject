from django.db import models

# Create your models here.

class price_2011_2020(models.Model):
    province_index = models.CharField(max_length=20, verbose_name="省份编号")
    province_name = models.CharField(max_length=20, verbose_name="省份")
    vegetable_index = models.CharField(max_length=20, verbose_name="蔬菜类型编号")
    vegetable_name = models.CharField(max_length=20, verbose_name="蔬菜类型")
    craft_index = models.CharField(max_length=20, verbose_name="蔬菜编号")
    craft_name = models.CharField(max_length=20, verbose_name="蔬菜名称")
    c_unit = models.CharField(max_length=20, verbose_name="单位")
    market_index = models.CharField(max_length=20, verbose_name="市场编号")
    market_name = models.CharField(max_length=80, verbose_name="市场名称")
    price_2011 = models.CharField(max_length=200, verbose_name="2011年数据")
    price_2012 = models.CharField(max_length=200, verbose_name="2012年数据")
    price_2013 = models.CharField(max_length=200, verbose_name="2013年数据")
    price_2014 = models.CharField(max_length=200, verbose_name="2014年数据")
    price_2015 = models.CharField(max_length=200, verbose_name="2015年数据")
    price_2016 = models.CharField(max_length=200, verbose_name="2016年数据")
    price_2017 = models.CharField(max_length=200, verbose_name="2017年数据")
    price_2018 = models.CharField(max_length=200, verbose_name="2018年数据")
    price_2019 = models.CharField(max_length=200, verbose_name="2019年数据")
    price_2020 = models.CharField(max_length=200, verbose_name="2020年数据")
    class Meta:
        verbose_name = verbose_name_plural = "2011-2020价格数据"
        db_table = "price_2011_2020"

class DailyPrice_BP(models.Model):
    market_index = models.CharField(max_length=20, verbose_name="市场编号")
    market_name = models.CharField(max_length=80, verbose_name="市场名称")
    brief = models.CharField(max_length=8000, verbose_name="市场简介")
    picture = models.BinaryField()
# python manage.py makemigrations
# python manage.py migrate
    class Meta:
        verbose_name = verbose_name_plural = "批发市场图文简介"
        db_table = "market_brief_picture"

class DailyPrice_DP(models.Model):
    market_index = models.CharField(max_length=20, verbose_name="市场编号")
    date = models.DateTimeField()
    craft_name = models.CharField(max_length=50, verbose_name="蔬菜名称")
    price = models.CharField(max_length=20, verbose_name="单价")

    class Meta:
        verbose_name = verbose_name_plural = "批发市场单日价格"
        db_table = "market_date_price"
