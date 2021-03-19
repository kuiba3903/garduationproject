"""将之间写入数据库的数据转存到现在所建立的数据库中"""
"""离线脚本"""

import pymysql
import os
import sys
import django


if __name__ == "__main__":
    conn = pymysql.connect(host="localhost", user="root",\
                                    password="qwer1234", db="db_2019_2020", charset="utf8mb4")
    cursor = conn.cursor()
    # 创建数据库的语句
    sql = "select * from price_2019_2020"
    count = cursor.execute(sql)
    print(count)
    res = cursor.fetchall()
    print(len(res))
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(base_dir)
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myweb.myweb.settings")
    django.setup()

    from price import models
    for item in res:
        print(res.index(item))
        # 写入数据库中
        models.Price.objects.create(
            province_index=item[1],
            province_name=item[2],
            vegetable_index=item[3],
            vegetable_name=item[4],
            craft_index=item[5],
            craft_name=item[6],
            c_unit=item[7],
            market_index=item[8],
            market_name=item[9],
            price_2019=item[10],
            price_2020=item[11]
        )