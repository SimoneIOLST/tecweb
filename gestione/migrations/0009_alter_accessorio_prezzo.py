# Generated by Django 4.2.4 on 2023-08-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0008_rename_marca_accessorio_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessorio',
            name='prezzo',
            field=models.FloatField(),
        ),
    ]
