# Generated by Django 4.2.4 on 2023-08-30 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestione', '0012_venditore_venditore'),
    ]

    operations = [
        migrations.CreateModel(
            name='OggettoCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessorio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestione.accessorio')),
                ('mezzo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestione.mezzo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carrello',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(related_name='cerrello', to='gestione.oggettocart')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Carrelli',
            },
        ),
    ]