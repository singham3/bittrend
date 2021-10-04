from .models import *
from rest_framework import serializers


class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = "__all__"
