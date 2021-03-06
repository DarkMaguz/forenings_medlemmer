# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-09 21:25
from __future__ import unicode_literals

from django.db import migrations, models

def clear_longtitude_latitude(apps, schema_editor):
    Department = apps.get_model('members', 'department')
    departments = Department.objects.all()
    for department in departments:
        department.longtitude = None
        department.latitude = None
        department.save()

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0096_merge'),
    ]

    operations = [
        migrations.RunPython(clear_longtitude_latitude),
    ]
