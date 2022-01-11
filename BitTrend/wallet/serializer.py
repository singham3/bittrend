from .models import *
from rest_framework import serializers


class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTransaction
        fields = "__all__"


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        extra_kwargs = {'token': {'write_only': True}}
        fields = "__all__"
