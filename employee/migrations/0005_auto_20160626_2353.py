# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_department_acronym'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.FileField(null=True, upload_to='photos'),
        ),
    ]
