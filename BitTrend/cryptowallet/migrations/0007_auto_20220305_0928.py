# Generated by Django 3.2.7 on 2022-03-05 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptowallet', '0006_auto_20220216_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptowallet',
            name='available_balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='cryptowallet',
            name='hold_balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='fills',
            field=models.TextField(blank=True, null=True, verbose_name=65500),
        ),
        migrations.AddField(
            model_name='order',
            name='origClientOrderId',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transactTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='withdraw_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='clientOrderId',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='cummulativeQuoteQty',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='executedQty',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='icebergQty',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='isWorking',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderId',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderListId',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='origQty',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='origQuoteOrderQty',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='side',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='stopPrice',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='timeInForce',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='updateTime',
            field=models.DateTimeField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='WithdrawHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('transactionFee', models.CharField(blank=True, max_length=255, null=True)),
                ('coin', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('Cancelled', '1'), ('Awaiting Approval', '2'), ('Rejected', '3'), ('Processing', '4'), ('Failure', '5'), ('Completed', '6')], max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('txId', models.CharField(blank=True, max_length=255, null=True)),
                ('network', models.CharField(blank=True, max_length=255, null=True)),
                ('transferType', models.CharField(blank=True, max_length=255, null=True)),
                ('info', models.CharField(blank=True, max_length=255, null=True)),
                ('confirmNo', models.CharField(blank=True, max_length=255, null=True)),
                ('walletType', models.CharField(blank=True, max_length=255, null=True)),
                ('txKey', models.CharField(blank=True, max_length=255, null=True)),
                ('applyTime', models.DateTimeField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='withdraw_order', to='cryptowallet.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_withdraw', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]