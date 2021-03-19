from django.db import models

# Create your models here.


class Price(models.Model):
    province_index = models.CharField(max_length=20, verbose_name="省份编号")
    province_name = models.CharField(max_length=20, verbose_name="省份")
    vegetable_index = models.CharField(max_length=20, verbose_name="蔬菜类型编号")
    vegetable_name = models.CharField(max_length=20, verbose_name="蔬菜类型")
    craft_index = models.CharField(max_length=20, verbose_name="蔬菜编号")
    craft_name = models.CharField(max_length=20, verbose_name="蔬菜名称")
    c_unit = models.CharField(max_length=20, verbose_name="单位")
    market_index = models.CharField(max_length=20, verbose_name="市场编号")
    market_name = models.CharField(max_length=80, verbose_name="市场名称")
    price_2019 = models.CharField(max_length=200, verbose_name="2019年数据")
    price_2020 = models.CharField(max_length=200, verbose_name="2020年数据")


    class Meta:
        verbose_name = verbose_name_plural = "2019-2020价格数据"
        db_table = "price_2019_2020"
