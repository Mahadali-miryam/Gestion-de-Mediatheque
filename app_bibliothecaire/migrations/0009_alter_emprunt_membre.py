# Generated by Django 5.1.5 on 2025-02-06 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0008_remove_cd_date_emprunt_remove_cd_date_retour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='membre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emprunts', to='app_bibliothecaire.membre'),
        ),
    ]
