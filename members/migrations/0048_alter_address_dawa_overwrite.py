# Generated by Django 4.2 on 2024-03-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0047_merge_20240329_2131"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="dawa_overwrite",
            field=models.BooleanField(
                default=False,
                help_text="\n    Lader dig gemme en anden længde- og breddegrad end oplyst fra DAWA     (hvor vi henter adressedata).     Spørg os i #medlemsssystem_support på Slack hvis du mangler hjælp.\n    ",
                verbose_name="Overskriv DAWA",
            ),
        ),
    ]