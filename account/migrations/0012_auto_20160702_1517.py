# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20160702_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradestep',
            name='nextStep',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='steps',
        ),
        migrations.DeleteModel(
            name='GradeStep',
        ),
    ]
