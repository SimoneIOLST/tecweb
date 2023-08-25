# Generated by Django 4.2.4 on 2023-08-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0009_alter_accessorio_prezzo'),
    ]

    operations = [
        migrations.AddField(
            model_name='venditore',
            name='citta',
            field=models.CharField(default='Modena', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venditore',
            name='nome',
            field=models.CharField(default='Modena', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venditore',
            name='provincia',
            field=models.CharField(default='Modena', max_length=50),
            preserve_default=False,
        ),
    ]