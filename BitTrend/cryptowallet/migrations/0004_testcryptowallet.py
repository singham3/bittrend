# Generated by Django 3.2.7 on 2022-01-11 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptowallet', '0003_cryptowallet_locked'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCryptoWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=20)),
                ('address', models.TextField(blank=True, max_length=20000, null=True)),
                ('network_address', models.TextField(blank=True, max_length=65500, null=True)),
                ('balance', models.FloatField(default=0.0)),
                ('locked', models.FloatField(default=0.0)),
                ('is_pool', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_test_crypto_wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]