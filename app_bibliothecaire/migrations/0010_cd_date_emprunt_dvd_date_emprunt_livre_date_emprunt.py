# Generated by Django 5.1.5 on 2025-02-13 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bibliothecaire', '0009_alter_emprunt_membre'),
    ]

    operations = [
        migrations.AddField(
            model_name='cd',
            name='date_emprunt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dvd',
            name='date_emprunt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='livre',
            name='date_emprunt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
