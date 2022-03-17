# Generated by Django 3.2.7 on 2022-02-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptowallet', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='clientOrderId',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='cummulativeQuoteQty',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='executedQty',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='icebergQty',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderId',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderListId',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='origQty',
            field=models.CharField(max_length=220),
        ),
        migrations.AlterField(
            model_name='order',
            name='origQuoteOrderQty',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='side',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='spot',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='stopPrice',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='symbol',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='timeInForce',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='updateTime',
            field=models.DateTimeField(max_length=200),
        ),
    ]
