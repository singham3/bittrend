from django.db import models
from BitTrend.account.models import User
# from django.contrib.postgres.fields import JSONField


class CryptoWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_crypto_wallet')
    coin = models.CharField(max_length=20)
    network = models.CharField(max_length=20, null=True, blank=True)
    seed = models.TextField(max_length=20000, null=True, blank=True)
    private_key = models.TextField(max_length=20000, null=True, blank=True)
    public_key = models.TextField(max_length=20000, null=True, blank=True)
    xprivate_key = models.TextField(max_length=20000, null=True, blank=True)
    xpublic_key = models.TextField(max_length=20000, null=True, blank=True)
    address = models.TextField(max_length=20000, null=True, blank=True)
    wif = models.TextField(max_length=20000, null=True, blank=True)
    network_address = models.TextField(max_length=65500, null=True, blank=True)
    balance = models.FloatField(default=0.0)
    available_balance = models.FloatField(default=0.0)
    hold_balance = models.FloatField(default=0.0)
    locked = models.FloatField(default=0.0)
    xpublic_key_prime = models.TextField(max_length=20000, null=True, blank=True)
    is_pool = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class TestCryptoWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_test_crypto_wallet')
    coin = models.CharField(max_length=20)
    address = models.TextField(max_length=20000, null=True, blank=True)
    network_address = models.TextField(max_length=65500, null=True, blank=True)
    balance = models.FloatField(default=0.0)
    locked = models.FloatField(default=0.0)
    is_pool = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    spot = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    orderId = models.BigIntegerField(null=True, blank=True)
    orderListId = models.BigIntegerField(null=True, blank=True)
    clientOrderId = models.CharField(max_length=200, null=True, blank=True)
    origClientOrderId = models.CharField(max_length=200, null=True, blank=True)
    transactTime = models.DateTimeField(null=True, blank=True)
    price = models.CharField(max_length=200, null=True, blank=True)
    origQty = models.CharField(max_length=220, null=True, blank=True)
    executedQty = models.CharField(max_length=200, null=True, blank=True)
    cummulativeQuoteQty = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    timeInForce = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    side = models.CharField(max_length=200, null=True, blank=True)
    fills = models.TextField(65500, null=True, blank=True)
    stopPrice = models.CharField(max_length=200, null=True, blank=True)
    icebergQty = models.CharField(max_length=200, null=True, blank=True)
    time = models.DateTimeField(max_length=200, null=True, blank=True)
    updateTime = models.DateTimeField(max_length=200, null=True, blank=True)
    isWorking = models.BooleanField(default=False, null=True, blank=True)
    origQuoteOrderQty = models.CharField(max_length=200, null=True, blank=True)
    withdraw_id = models.CharField(max_length=255, null=True, blank=True)


status = (
    ('1', 'Cancelled' ),
    ('2', 'Awaiting Approval'),
    ('3', 'Rejected'),
    ('4', 'Processing'),
    ('5', 'Failure'),
    ('6', 'Completed'),
)


class WithdrawHistory(models.Model):
    bid = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_withdraw', null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='withdraw_order', null=True)
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.SET_NULL, null=True, related_name="crypto_wallet_withdraw")
    amount = models.CharField(max_length=255, null=True, blank=True)
    transactionFee = models.CharField(max_length=255, null=True, blank=True)
    coin = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=status, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    txId = models.CharField(max_length=255, null=True, blank=True)
    network = models.CharField(max_length=255, null=True, blank=True)
    transferType = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    confirmNo = models.CharField(max_length=255, null=True, blank=True)
    walletType = models.CharField(max_length=255, null=True, blank=True)
    txKey = models.CharField(max_length=255, null=True, blank=True)
    applyTime = models.DateTimeField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class DepositHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_deposit")
    wallet = models.ForeignKey(CryptoWallet, on_delete=models.SET_NULL, null=True, related_name="crypto_wallet_deposit")
    amount = models.CharField(max_length=255, null=True, blank=True)
    withdraw_id = models.CharField(max_length=255, null=True, blank=True)
    coin = models.CharField(max_length=255, null=True, blank=True)
    network = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=status, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    addressTag = models.CharField(max_length=255, null=True, blank=True)
    txId = models.CharField(max_length=255, null=True, blank=True)
    insertTime = models.DateTimeField(null=True, blank=True)
    transferType = models.IntegerField()
    unlockConfirm = models.IntegerField()
    walletType = models.IntegerField()
    confirmTimes = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
