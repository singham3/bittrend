# Generated by Django 3.2.7 on 2022-01-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptowallet', '0002_cryptowallet_network_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptowallet',
            name='locked',
            field=models.FloatField(default=0.0),
        ),
    ]
