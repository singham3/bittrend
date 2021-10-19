import datetime
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from .serializer import *
from .models import CryptoWallet
from account.middleware import TokenAuthenticationMiddleware
from blockcypher import get_total_balance, simple_spend, create_unsigned_tx


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

            # simple_spend(from_privkey='514d70665890269e10187343536febe4de71ad2a980ba5cb355ece31cd7a4de9',
            #              to_address='DLapXSU24kPuutR7jJBCdpNh3TQNucW4w9', to_satoshis=100000000, coin_symbol='doge',
            #              api_key="9dfc12062dcd48c29e1a2cbcd919b251")
            inputs = [{'address': 'D7D291X5DtRArCvvpF1aGXx1ciUMv9hmTb'}, ]
            outputs = [{'address': 'DLapXSU24kPuutR7jJBCdpNh3TQNucW4w9', 'value': 1000000}]
            unsigned_tx = create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='doge', api_key="9dfc12062dcd48c29e1a2cbcd919b251")
            return Response({"data": unsigned_tx, "message": "transaction list", "isSuccess": True, "status": 200},
                            status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 400}, status=200)
    return Response({"data": None, "message": "coin is required", "isSuccess": False, "status": 404}, status=200)
