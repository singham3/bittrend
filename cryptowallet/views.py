import datetime
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from .serializer import *
from .models import CryptoWallet
from account.middleware import TokenAuthenticationMiddleware
from blockcypher import get_total_balance


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_balance_view(request, coin=None):
    if coin:
        if request.user.is_authenticated:
            obj = CryptoWallet.objects.filter(user=request.user, coin=coin).first()
            balance = get_total_balance(obj.address, coin_symbol=coin) / 100000000
            obj.balance = balance
            obj.updated_at = datetime.datetime.now()
            obj.save()
            return Response({"data": CryptoWalletSerializer(instance=obj, many=False).data,
                             "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 400}, status=200)
    return Response({"data": None, "message": "coin is required", "isSuccess": False, "status": 404}, status=200)


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_transactions_view(request, coin=None):
    if coin:
        if request.user.is_authenticated:
            obj = CryptoWallet.objects.filter(user=request.user, coin__icontains=coin).first()

            return Response({"data": "transaction", "message": "transaction list", "isSuccess": True, "status": 200},
                            status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 400}, status=200)
    return Response({"data": None, "message": "coin is required", "isSuccess": False, "status": 404}, status=200)
