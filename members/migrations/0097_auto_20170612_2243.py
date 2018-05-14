# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-12 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Family = apps.get_model("members", "Family")
    for i in Family.objects.all():
        i.unique = uuid.UUID(str(i.unique))
        i.save()

    EmailItem = apps.get_model("members", "EmailItem")
    for i in EmailItem.objects.all():
        i.bounce_token = uuid.UUID(str(i.bounce_token))
        i.save()


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0096_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailitem',
            name='bounce_token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='family',
            name='unique',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        # Convert the formats of UUID fields
        migrations.RunPython(forwards_func),

    ]
