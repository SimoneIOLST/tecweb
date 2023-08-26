# Generated by Django 4.2.4 on 2023-08-26 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestione', '0010_venditore_citta_venditore_nome_venditore_provincia'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteMezzo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mezzo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.mezzo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Mezzi favoriti',
                'unique_together': {('user', 'mezzo')},
            },
        ),
        migrations.CreateModel(
            name='FavouriteAccessorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestione.accessorio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Accessori favoriti',
                'unique_together': {('user', 'acc')},
            },
        ),
    ]