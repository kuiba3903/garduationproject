# Generated by Django 2.2.2 on 2021-01-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPrice_BP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_index', models.CharField(max_length=20, verbose_name='市场编号')),
                ('market_name', models.CharField(max_length=80, verbose_name='市场名称')),
                ('brief', models.CharField(max_length=8000, verbose_name='市场简介')),
                ('picture', models.BinaryField()),
            ],
            options={
                'verbose_name': '批发市场图文简介',
                'verbose_name_plural': '批发市场图文简介',
                'db_table': 'market_brief_picture',
            },
        ),
        migrations.CreateModel(
            name='DailyPrice_DP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_index', models.CharField(max_length=20, verbose_name='市场编号')),
                ('date', models.DateTimeField()),
                ('craft_name', models.CharField(max_length=50, verbose_name='蔬菜名称')),
                ('price', models.CharField(max_length=20, verbose_name='单价')),
            ],
            options={
                'verbose_name': '批发市场单日价格',
                'verbose_name_plural': '批发市场单日价格',
                'db_table': 'market_date_price',
            },
        ),
    ]
