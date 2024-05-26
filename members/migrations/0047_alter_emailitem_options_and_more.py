# Generated by Django 4.2.11 on 2024-05-23 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0046_alter_department_options_alter_union_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emailitem",
            options={
                "ordering": ["-created_dtm"],
                "verbose_name": "Email",
                "verbose_name_plural": "Emails",
            },
        ),
        migrations.RenameField(
            model_name="emailitem",
            old_name="reciever",
            new_name="receiver",
        ),
    ]
