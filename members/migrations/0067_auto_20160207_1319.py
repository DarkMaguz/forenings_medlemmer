# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-07 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0066_auto_20160206_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='has_waiting_list',
            field=models.BooleanField(default=True, verbose_name='Venteliste'),
        ),
    ]