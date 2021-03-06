# Generated by Django 3.2.7 on 2022-03-02 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptowallet', '0006_auto_20220216_0716'),
        ('wallet', '0004_accounttransaction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwallet',
            name='total_hold_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='HoldAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_for', to='cryptowallet.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet_hold_amount', to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet_amount_hold', to='wallet.userwallet')),
            ],
        ),
    ]
