# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_auto_20160731_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='last_name',
        ),
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contact',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Contact'),
        ),
    ]
