# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='designation',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='employeeincrement',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workhistory',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]