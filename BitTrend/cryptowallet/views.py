import datetime
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .serializer import *
from .models import *
from ..wallet.models import UserWallet, HoldAmount
from BitTrend.account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from django.conf import settings
from binance.error import ClientError
import json
import logging
import pytz
from ..wallet.models import UserWallet
from django.db.models import Q, Sum, F
from blockcypher import get_address_overview, create_unsigned_tx
import numpy as np
from pywallet import wallet


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_balance_view(request, coin=None):
    if request.user.is_superuser:
        for i in settings.CLIENT.account()['balances']:
            CryptoWallet.objects.filter(user=request.user, coin=i['asset']).update(
                balance=i['free'],
                locked=i['locked'],
                updated_at=datetime.datetime.now()
            )
        return Response({"data": None, "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)
    else:
        wallet = CryptoWallet.objects.filter(user=request.user, coin__icontains=coin)
        if wallet.exists():
            balance = get_address_overview(wallet.first().address, api_key='9dfc12062dcd48c29e1a2cbcd919b251', coin_symbol=coin)
            if balance:
                wallet.update(balance=balance['final_balance'] / 100000000,
                              available_balance=balance['total_received'] / 100000000,
                              hold_balance=balance['unconfirmed_balance'] / 100000000
                              )
    serializer = CryptoWalletSerializer(instance=CryptoWallet.objects.filter(user=request.user, coin__icontains=coin), many=True)
    return Response({"data": serializer.data, "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_test_crypto_wallet_get_balance_view(request, coin=None):
    if request.user.is_superuser:
        for i in settings.TEST_CLIENT.account()['balances']:
            if TestCryptoWallet.objects.filter(user=request.user, coin=i['asset']).exists():
                TestCryptoWallet.objects.filter(user=request.user, coin=i['asset']).update(
                    balance=i['free'],
                    locked=i['locked'],
                    updated_at=datetime.datetime.now()
                )
            else:
                TestCryptoWallet.objects.create(user=request.user, coin=i['asset'], balance=i['free'],
                                                locked=i['locked'], is_pool=True)
        return Response({"data": None, "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_view(request):
    if request.user.is_authenticated:
        obj = CryptoWallet.objects.filter(user=request.user)
        if not obj.exists():
            seed = wallet.generate_mnemonic()
            for coin in ['eth', 'doge', 'btc', 'btg', 'bch', 'ltc', 'dash', 'qtum']:
                k = wallet.create_wallet(seed=seed, children=0, network=coin)
                CryptoWallet.objects.create(user=request.user, coin=coin, seed=k['seed'], private_key=k['private_key'],
                                            public_key=k['public_key'], xprivate_key=k['xprivate_key'], xpublic_key=k['xpublic_key'],
                                            wif=k['wif'], xpublic_key_prime=k['xpublic_key_prime'], address=k['address'], network=coin)
            obj = CryptoWallet.objects.filter(user=request.user)
        serializer = CryptoWalletSerializer(instance=obj, many=True)
        return Response({"data": serializer.data, "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 404}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def admin_crypto_wallet_get_view(request, coin=None):
    if not request.user.is_authenticated:
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 404}, status=200)
    else:
        if coin:
            obj = CryptoWallet.objects.filter(user__is_superuser=True, coin=coin.upper()).first()
            many = False
        else:
            q = Q()
            for i in ['eth', 'doge', 'btc', 'btg', 'bch', 'ltc', 'dash', 'qtum']:
                q |= Q(coin=i.upper())
            q &= Q(user__is_superuser=True)
            obj = CryptoWallet.objects.filter(q)
            many = True
        serializer = AdminCryptoWalletSerializer(instance=obj, many=many)
        return Response({"data": serializer.data, "message": "crypto wallet", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(CreateTestOrderMiddleware)
def user_crypto_wallet_create_test_order_view(request, form=None):
    try:
        response = settings.TEST_CLIENT.new_order_test(**{k: v for k, v in form.cleaned_data.items() if v})
        if response:
            response['user'] = request.user
            response['spot'] = "test"
            Order.objects.create(**response)
        return Response(
            {"data": response, "message": "Successfully Test order created", "isSuccess": True, "status": 200},
            status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500},
                        status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_test_order_view(request, symbol=None):
    try:
        response = settings.TEST_CLIENT.get_orders(symbol)
        if response:
            for i in response:
                if not Order.objects.filter(orderId=i['orderId']).exists():
                    response['user'] = request.user
                    response['spot'] = "test"
                    Order.objects.create(**response)
        return Response(
            {"data": response, "message": "Successfully GET Test order details", "isSuccess": True, "status": 200},
            status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500},
                        status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(CancelTestOrderMiddleware)
def user_crypto_wallet_cancel_test_order_view(request, form):
    try:
        symbol = form.cleaned_data.get('symbol')
        orderId = form.cleaned_data.get('orderId')
        response = settings.TEST_CLIENT.cancel_order(symbol, orderId=orderId)
        return Response(
            {"data": response, "message": "Successfully GET Test order details", "isSuccess": True, "status": 200},
            status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500},
                        status=200)


def mainnet_sell_order(user, address, query, price):
    coin = query['symbol'].replace('USDT', '').replace('TRY', '').lower()
    admin_address = CryptoWallet.objects.filter(user_email="admin@bittrend.io", coin__icontains=coin)
    inputs = [{'address': address}, ]
    outputs = [{'address': admin_address.network_address[coin.upper()], 'value': query['quantity'] * price}]
    unsigned_tx = create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol=coin, api_key='9dfc12062dcd48c29e1a2cbcd919b251')


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(CreateTestOrderMiddleware)
def user_crypto_wallet_create_new_order_view(request, form=None):
    try:
        wallet, created = UserWallet.objects.get_or_create(user=request.user)
        query = {k: v for k, v in form.cleaned_data.items() if v}
        if query['type'] == 'MARKET':
            price = float(settings.CLIENT.ticker_price(query['symbol'])['price'])
        else:
            price = query['price']
        address = CryptoWallet.objects.filter(user=request.user, coin__icontains=query['symbol'].replace('USDT', '').replace('TRY', ''))
        if not address.exists():
            return Response({"data": None, "message": "Token Currently not available", "isSuccess": False, "status": 500}, status=200)
        if wallet.amount >= query['quantity'] * price:
            if query['type'] == "SELL":
                res = mainnet_sell_order(request.user, address.first().address, query, price)
                return Response({"data": res, "message": "order not created", "isSuccess": False, "status": 500}, status=200)
            response = settings.CLIENT.new_order(**query)
            if response:
                if 'time' in response:
                    response['time'] = datetime.datetime.fromtimestamp(response['time'] / 1000, pytz.timezone("UTC"))
                if 'updateTime' in response:
                    response['updateTime'] = datetime.datetime.fromtimestamp(response['updateTime'] / 1000, pytz.timezone("UTC"))
                if 'transactTime' in response:
                    response['transactTime'] = datetime.datetime.fromtimestamp(response['transactTime'] / 1000, pytz.timezone("UTC"))
                if 'fills' in response:
                    response['fills'] = str(response['fills'])
                response['user'] = request.user
                response['spot'] = "test"
                order = Order.objects.create(**response)
                if response['status'] == 'FILLED':
                    symbol = order.symbol.replace('USDT', '').replace('TRY', '')
                    wh_id = settings.CLIENT.withdraw(coin=symbol, amount=order.origQty, address=address.first().address)
                    order.withdraw_id = wh_id['id']
                    order.save()
                    wh = settings.CLIENT.withdraw_history()[0]
                    wh['applyTime'] = datetime.datetime.strptime(wh['applyTime'], '%Y-%m-%d %H:%M:%S')
                    wh['bid'] = wh['id']
                    wh['user'] = request.user
                    wh['order'] = order
                    wh.pop('id')
                    wh_serializer = WithdrawHistorySerializer(data=wh)
                    if wh_serializer.is_valid():
                        wh_serializer.save()
                    else:
                        error = wh_serializer.errors
                        error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": True, "status": 500}, status=200)
                else:
                    param = {'user': request.user, 'wallet': wallet, 'order': order, 'amount': query['quantity'] * price}
                    HoldAmount.objects.create(**param)
                    wallet.total_hold_amount = HoldAmount.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']
                wallet.amount = wallet.amount - query['quantity'] * price
                wallet.updated_at = datetime.datetime.now()
                wallet.save()
                data = CryptoOrderSerializer(instance=order).data
                return Response({"data": data, "message": "Successfully order created", "isSuccess": True, "status": 200}, status=200)
            return Response({"data": response, "message": "order not created", "isSuccess": False, "status": 500}, status=200)
        else:
            return Response({"data": None, "message": "insufficient Fund", "isSuccess": False, "status": 500}, status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_crypto_wallet_get_mainnet_order_view(request, mode=None, symbol=None):
    try:
        response = settings.CLIENT.get_orders(symbol)
        if response:
            for i in response:
                i['time'] = datetime.datetime.fromtimestamp(i['time'] / 1000, pytz.timezone("UTC"))
                i['updateTime'] = datetime.datetime.fromtimestamp(i['updateTime'] / 1000, pytz.timezone("UTC"))
                if not Order.objects.filter(orderId=i['orderId']).exists():
                    i['user'] = request.user
                    i['spot'] = "mainnet"
                    Order.objects.create(**i)
                else:
                    Order.objects.filter(orderId=i['orderId']).update(**i)
        if mode:
            if mode == 'HISTORY':
                obj = Order.objects.filter(user=request.user, symbol=symbol).order_by('-time')
            else:
                obj = Order.objects.filter(
                    Q(status__icontains=mode) | Q(side__icontains=mode) | Q(type__icontains=mode) | Q(orderId__icontains=mode),
                    user=request.user, symbol=symbol).order_by('-time')
        else:
            obj = Order.objects.filter(user=request.user, symbol=symbol).order_by('-time')
        data = CryptoOrderSerializer(instance=obj, many=True).data
        return Response({"data": data, "message": "Successfully get order details", "isSuccess": True, "status": 200}, status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(CancelTestOrderMiddleware)
def user_crypto_wallet_cancel_mainnet_order_view(request, form):
    try:
        symbol = form.cleaned_data.get('symbol')
        orderId = form.cleaned_data.get('orderId')
        order = Order.objects.filter(orderId=orderId)
        if order.exists():
            response = settings.CLIENT.cancel_order(symbol, orderId=orderId)
            if response:
                if 'time' in response:
                    response['time'] = datetime.datetime.fromtimestamp(response['time'] / 1000, pytz.timezone("UTC"))
                if 'updateTime' in response:
                    response['updateTime'] = datetime.datetime.fromtimestamp(response['updateTime'] / 1000, pytz.timezone("UTC"))
                if 'transactTime' in response:
                    response['transactTime'] = datetime.datetime.fromtimestamp(response['transactTime'] / 1000, pytz.timezone("UTC"))
                if 'fills' in response:
                    response['fills'] = str(response['fills'])
                order.update(**response)
                if HoldAmount.objects.filter(order=order.first()).exists():
                    hold_amount = HoldAmount.objects.get(order=order.first())
                    UserWallet.objects.filter(user=request.user).update(
                        amount=F('amount') + hold_amount.amount,
                        total_hold_amount=F('total_hold_amount') - hold_amount.amount,
                        updated_at=datetime.datetime.now())
                    hold_amount.delete()
                return Response(
                    {"data": response, "message": "Successfully Cancel order", "isSuccess": True, "status": 200},
                    status=200)
            return Response(
                {"data": response, "message": "Order cancellation request failed ", "isSuccess": False, "status": 500},
                status=200)
        return Response({"data": None, "message": "Order not found", "isSuccess": False, "status": 404}, status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message)['msg'], "isSuccess": False, "status": 500},
                        status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(CryptoPriceCalculatorMiddleware)
def crypto_price_calculator(request, symbol, form):
    form.cleaned_data['symbol'] = symbol
    form.cleaned_data['cur_price'] = float(settings.CLIENT.ticker_price(symbol)['price'])
    if form.cleaned_data['type'] == "MARKET":
        form.cleaned_data['price'] = form.cleaned_data['cur_price']
    price = form.cleaned_data['quantity'] * form.cleaned_data['price']
    form.cleaned_data['min_qty'] = 10 / form.cleaned_data['price']
    form.cleaned_data['fee'] = price * 0.012
    form.cleaned_data['order_price'] = price + form.cleaned_data['fee']
    if price < 10:
        return Response({"data": form.cleaned_data, "message": "Order Value should grater then 10$", "isSuccess": False,
                         "status": 500}, status=200)
    else:
        return Response({"data": form.cleaned_data, "message": "ok", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
def withdrawal_history(request):
    try:
        withdraw_history = settings.CLIENT.withdraw_history()
        for wh in withdraw_history:
            order = Order.objects.filter(withdraw_id=wh['id'])
            if order.exists():
                wh['order'] = order
                wh['user'] = order.user
            dh = DepositHistory.objects.filter(withdraw_id=wh['id'])
            if dh.exists():
                wh['wallet'] = dh.wallet
                wh['user'] = dh.user
            wh['applyTime'] = datetime.datetime.strptime(wh['applyTime'], '%Y-%m-%d %H:%M:%S')
            wh['bid'] = wh['id']
            wh.pop('id')
            wh_serializer = WithdrawHistorySerializer(data=wh)
            if wh_serializer.is_valid():
                wh_serializer.save()
            else:
                error = wh_serializer.errors
                error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                return Response({"data": None, "message": error, "isSuccess": True, "status": 500}, status=200)
        return Response({"data": withdraw_history, "message": "ok", "isSuccess": True, "status": 200}, status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message), "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def deposit_history(request):
    try:
        deposit_history = settings.CLIENT.deposit_history()
        serializer = DepositHistorySerializer(data=deposit_history, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            error = serializer.errors
            logging.error(error)
        if request.method == "POST":
            txId = request.POST.get('txId')
            dh = DepositHistory.objects.filter(txId=txId, user__isnull=True, wallet__isnull=True)
            if dh.exists():
                cw = CryptoWallet.objects.filter(user=request.user, coin__icontains=dh.first().coin)
                if cw.exists():
                    wh_id = settings.CLIENT.withdraw(coin=dh.first().coin, amount=dh.first().amount, address=cw.first().address)
                    dh.update(wallet=cw.first(), user=request.user, withdraw_id=wh_id['id'])
                    wh = settings.CLIENT.withdraw_history()[0]
                    wh['applyTime'] = datetime.datetime.strptime(wh['applyTime'], '%Y-%m-%d %H:%M:%S')
                    wh['bid'] = wh['id']
                    wh['user'] = request.user
                    wh['wallet'] = cw.first()
                    wh.pop('id')
                    wh_serializer = WithdrawHistorySerializer(data=wh)
                    if wh_serializer.is_valid():
                        wh_serializer.save()
                    else:
                        error = wh_serializer.errors
                        error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": True, "status": 500}, status=200)
                else:
                    return Response(
                        {"data": None, "message": f"{dh.first().coin} address not created yet in your wallet", "isSuccess": False, "status": 200},
                        status=200)
            else:
                return Response({"data": None, "message": f"Transaction not exists", "isSuccess": False, "status": 200}, status=200)
        else:
            dh = DepositHistory.objects.filter(user=request.user)
            serializer = DepositHistorySerializer(instance=dh, many=True).data
            return Response({"data": serializer, "message": f"Get user`s deposits", "isSuccess": False, "status": 200}, status=200)
    except ClientError as error:
        return Response({"data": None, "message": json.loads(error.message), "isSuccess": False, "status": 500}, status=200)
