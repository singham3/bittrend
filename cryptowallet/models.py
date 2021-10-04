from django.db import models
from account.models import User


class CryptoWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_crypto_wallet")
    coin = models.CharField(max_length=20)
    seed = models.TextField(max_length=20000, null=True, blank=True)
    private_key = models.TextField(max_length=20000, null=True, blank=True)
    public_key = models.TextField(max_length=20000, null=True, blank=True)
    xprivate_key = models.TextField(max_length=20000, null=True, blank=True)
    xpublic_key = models.TextField(max_length=20000, null=True, blank=True)
    address = models.TextField(max_length=20000, null=True, blank=True)
    wif = models.TextField(max_length=20000, null=True, blank=True)
    balance = models.FloatField(default=0.0)
    xpublic_key_prime = models.TextField(max_length=20000, null=True, blank=True)
    is_pool = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
