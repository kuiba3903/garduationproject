# Generated by Django 2.2.2 on 2020-12-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='price_2019',
            field=models.CharField(max_length=200, verbose_name='2019年数据'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_2020',
            field=models.CharField(max_length=200, verbose_name='2020年数据'),
        ),
    ]
