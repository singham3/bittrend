from django.db import models
from ..account.models import User
from ..cryptowallet.models import Order


class UserWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account_wallet")
    amount = models.FloatField(default=0.0)
    total_hold_amount = models.FloatField(default=0.0)
    token = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class AccountTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account_transaction", null=True, blank=True)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gross_amount = models.FloatField(default=0.0)
    net_amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=250, default="USD")
    paymentId = models.CharField(max_length=250)
    PayerID = models.CharField(max_length=250)
    fees = models.FloatField(default=0.0)
    admin_fees = models.FloatField(default=3.0)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HoldAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wallet_hold_amount")
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, related_name="user_wallet_amount_hold")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name="order_for", null=True)
    amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
