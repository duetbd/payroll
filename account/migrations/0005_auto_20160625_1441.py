# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20160624_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarysheet',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='salarysheet',
            name='modified_date',
        ),
        migrations.AlterField(
            model_name='allowancededuction',
            name='value',
            field=models.IntegerField(blank=True, null=True, verbose_name='Default Value'),
        ),
    ]
