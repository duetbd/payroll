# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import employee.managers


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20160703_0031'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='employee',
            managers=[
                ('objects', employee.managers.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(default='sabah@gmail.com', max_length=254, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='employee',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(default='123', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='designation',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='account.Grade', verbose_name='Grade'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.Department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.Designation', verbose_name='Designation'),
        ),
    ]
