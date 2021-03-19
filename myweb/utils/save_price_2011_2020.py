"""将之间写入数据库的数据转存到现在所建立的数据库中"""
"""离线脚本"""

import pymysql
import pandas as pd
import os
import sys
import django


if __name__ == "__main__":
    res = pd.read_csv("./price_2011_2020.csv",header=0)
    print(res)
    print(len(res))
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(base_dir)
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.myweb.settings")
    django.setup()

    from DailyPrice import models
    for i in range(len(res)):
        item = res.iloc[i]
        # 写入数据库中
        models.price_2011_2020.objects.create(
            province_index=item[1],
            province_name=item[2],
            vegetable_index=item[3],
            vegetable_name=item[4],
            craft_index=item[5],
            craft_name=item[6],
            c_unit=item[7],
            market_index=item[8],
            market_name=item[9],
            price_2011=item[10],
            price_2012=item[11],
            price_2013=item[12],
            price_2014=item[13],
            price_2015=item[14],
            price_2016=item[15],
            price_2017=item[16],
            price_2018=item[17],
            price_2019=item[18],
            price_2020=item[19]

        )