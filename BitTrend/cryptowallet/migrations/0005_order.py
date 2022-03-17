# Generated by Django 3.2.7 on 2022-01-11 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptowallet', '0004_testcryptowallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot', models.CharField(max_length=20)),
                ('symbol', models.CharField(max_length=20)),
                ('orderId', models.FloatField()),
                ('orderListId', models.CharField(max_length=20)),
                ('clientOrderId', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('origQty', models.FloatField()),
                ('executedQty', models.FloatField()),
                ('cummulativeQuoteQty', models.FloatField()),
                ('status', models.CharField(max_length=20)),
                ('timeInForce', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('side', models.CharField(max_length=20)),
                ('stopPrice', models.FloatField()),
                ('icebergQty', models.FloatField()),
                ('time', models.DateTimeField(max_length=20)),
                ('updateTime', models.DateTimeField(max_length=20)),
                ('isWorking', models.BooleanField(default=False)),
                ('origQuoteOrderQty', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]