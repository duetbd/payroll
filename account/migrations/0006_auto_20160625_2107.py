# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 15:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20160625_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarysheet',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='salarysheet',
            name='isFreezed',
            field=models.BooleanField(default=False, verbose_name='Freezed'),
        ),
        migrations.AlterField(
            model_name='salarysheetdetails',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
