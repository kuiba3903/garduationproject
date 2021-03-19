"""
    将爬取的每日农产品价格导入到数据库中
"""

import pymysql
import os
import sys
import django
import pandas as pd



if __name__ == "__main__":
    res = pd.read_csv("./market_price_first_3.csv", header=0)
    print(res)
    print(len(res))
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(base_dir)
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.myweb.settings")
    django.setup()
    # print(res.iloc[0][0])
    #
    from DailyPrice import models
    for i in range(len(res)):
        item = res.iloc[i]
        # 写入数据库中
        models.DailyPrice_BP.objects.create(
            market_index=item[1],
            market_name=item[2],
            brief=item[3],
            picture=item[4].encode("utf-8")
        )
    print("---------------")
    # data = pd.read_csv("./market_price_last_3.csv", header=0)
    # print(len(data))
    # for i in range(len(data)):
    #     item = data.iloc[i]
    #     models.DailyPrice_DP.objects.create(
    #         market_index=item[1],
    #         date=item[2],
    #         craft_name=item[3],
    #         price=item[4]
    #     )