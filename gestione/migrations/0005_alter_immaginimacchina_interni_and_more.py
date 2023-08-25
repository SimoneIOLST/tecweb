# Generated by Django 4.2.4 on 2023-08-23 14:41

from django.db import migrations, models
import gestione.models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0004_alter_immaginimacchina_interni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immaginimacchina',
            name='interni',
            field=models.ImageField(blank=True, null=True, upload_to=gestione.models.ImmaginiMacchina.uploadTo),
        ),
        migrations.AlterField(
            model_name='immaginimacchina',
            name='retro',
            field=models.ImageField(blank=True, null=True, upload_to=gestione.models.ImmaginiMacchina.uploadTo),
        ),
    ]