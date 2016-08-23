# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_auto_20160702_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='type',
            field=models.CharField(choices=[('', '----'), ('ac', 'Academic'), ('ad', 'Administrative')], max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='designation',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Grade', verbose_name='Grade'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='category',
            field=models.CharField(choices=[('', '----'), ('t', 'Teacher'), ('o', 'Officer'), ('s', 'Stuff')], default='t', max_length=1, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('', '----'), ('m', 'Male'), ('f', 'Female')], default='m', max_length=1, verbose_name='Gender'),
        ),
    ]
