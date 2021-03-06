# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20160703_0055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeallowancededuction',
            options={'ordering': ['allowance_deduction__order']},
        ),
        migrations.AlterModelOptions(
            name='salarysheetdetails',
            options={'ordering': ['allowance_deduction__order']},
        ),
        migrations.AlterField(
            model_name='salarysheet',
            name='isWithdrawan',
            field=models.BooleanField(default=True, verbose_name='Withdrawn'),
        ),
        migrations.AlterUniqueTogether(
            name='allowancedeductionemployeeclassvalue',
            unique_together=set([('employee_class', 'allowance_deduction')]),
        ),
    ]
