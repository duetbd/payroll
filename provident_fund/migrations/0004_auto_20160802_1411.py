# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provident_fund', '0003_auto_20160802_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlylogforgpf',
            name='interest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Interest'),
        ),
        migrations.AlterField(
            model_name='monthlylogforgpf',
            name='subscription',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Subscription'),
        ),
        migrations.AlterField(
            model_name='providentfundprofile',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Credit'),
        ),
    ]
