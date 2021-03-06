# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_auto_20160731_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Last Name'),
        ),
    ]
