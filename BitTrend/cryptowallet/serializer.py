from .models import *
from rest_framework import serializers
from datetime import datetime
import pytz


class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = "__all__"


class AdminCryptoWalletSerializer(serializers.ModelSerializer):
    network_address = serializers.SerializerMethodField()

    class Meta:
        model = CryptoWallet
        fields = ('id', 'coin', 'network_address', 'is_pool')

    def get_network_address(self, obj):
        data = eval(obj.network_address)
        return list(filter(lambda x: x["network"] == obj.coin, data))


class CryptoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class WithdrawHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawHistory
        fields = "__all__"


class DepositHistorySerializer(serializers.ModelSerializer):
    insertTime = serializers.IntegerField(write_only=True)

    class Meta:
        model = DepositHistory
        fields = "__all__"

    def create(self, data):
        data['insertTime'] = datetime.fromtimestamp(data['insertTime'] / 1000, pytz.timezone("UTC"))
        obj = DepositHistory.objects.filter(txId=data['txId'])
        if not obj.exists():
            return DepositHistory.objects.create(**data)
        else:
            return obj.first()


class GetCryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = ('coin', 'network_address')
