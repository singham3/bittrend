import paypalrestsdk
from django.conf import settings
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from .serializer import *
from BitTrend.account.middleware import TokenAuthenticationMiddleware
from .models import AccountTransaction, UserWallet
from django.db.models import F

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def test_paypal_payment_create_view(request):
    if request.user.is_authenticated:
        amount = request.POST.get('amount')

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://192.168.29.72:8000/api/v1/user/account/wallet/test/payment/return/",
                "cancel_url": "http://192.168.29.72:8000/api/v1/user/account/wallet/test/payment/cancel/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Wallet",
                        "sku": "Wallet",
                        "price": amount,
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": amount,
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    token = approval_url.split('&token=')[1]
                    if UserWallet.objects.filter(user=request.user).exists():
                        UserWallet.objects.filter(user=request.user).update(token=token)
                    else:
                        UserWallet.objects.create(user=request.user, token=token)
                    return Response({"data": approval_url, "message": "Payment created successfully", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": payment.error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
def test_paypal_payment_return_view(request):
    payment = paypalrestsdk.Payment.find(request.GET['paymentId'])
    if payment.execute({"payer_id": request.GET['PayerID']}):
        if payment.success():
            fees = float(payment.transactions[0].related_resources[0].sale.transaction_fee.value)
            gross_amount = float(payment.transactions[0].amount.total)
            if UserWallet.objects.filter(token=request.GET['token']).exists():
                user_wallet = UserWallet.objects.filter(token=request.GET['token'])
                AccountTransaction(user=user_wallet.first().user, email=payment.payer.payer_info.email,
                                   first_name=payment.payer.payer_info.first_name,
                                   last_name=payment.payer.payer_info.last_name,
                                   gross_amount=gross_amount,
                                   net_amount=gross_amount-fees-3.0, currency=payment.transactions[0].amount.currency,
                                   paymentId=payment.id, PayerID=payment.payer.payer_info.payer_id, fees=fees, is_success=True
                                   ).save()
                user_wallet.update(token=None, amount=F('amount') + (gross_amount-fees-3.0), is_active=True)
                UserWallet.objects.filter(user__is_superuser=True).update(amount=F('amount') + 3.0)
        return Response({"data": paypalrestsdk.Payment.find(request.GET['paymentId']).to_dict(),
                         "message": "GET callback details", "isSuccess": True, "status": 200}, status=200)
    else:
        return Response({"data": payment.to_dict(), "message": payment.error, "isSuccess": False, "status": 500}, status=200)


@api_view(['GET'])
def test_paypal_payment_cancel_view(request):
    return Response({"data": request.GET, "message": "GET cancel details", "isSuccess": True, "status": 200}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def test_paypal_payment_get_all_view(request):
    if request.user.is_authenticated:
        if AccountTransaction.objects.filter(user=request.user).exists():
            serializer = AccountTransactionSerializer(instance=AccountTransaction.objects.filter(user=request.user), many=True)
            return Response({"data": serializer.data, "message": "GET callback details", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "Transaction Not Found", "isSuccess": False, "status": 404}, status=200)
    return Response({"data": None, "message": "Unauthorised User", "isSuccess": False, "status": 404}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def test_paypal_payment_get_view(request, id=None, paymentId=None):
    if request.user.is_authenticated:
        if id:
            if AccountTransaction.objects.filter(user=request.user, id=id).exists():
                instance = AccountTransaction.objects.get(user=request.user, id=id)
            else:
                return Response({"data": None, "message": "Transaction Not Found", "isSuccess": False, "status": 404}, status=200)
        elif paymentId:
            if AccountTransaction.objects.filter(user=request.user, paymentId=paymentId).exists():
                instance = AccountTransaction.objects.get(user=request.user, paymentId=paymentId)
            else:
                return Response({"data": None, "message": "Transaction Not Found", "isSuccess": False, "status": 404}, status=200)
        serializer = AccountTransactionSerializer(instance=instance, many=False)
        return Response({"data": serializer.data, "message": "GET callback details", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorised User", "isSuccess": False, "status": 404}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_wallet_get_view(request):
    if request.user.is_authenticated:
        serializer = UserWalletSerializer(instance=UserWallet.objects.filter(user=request.user), many=True)
        return Response({"data": serializer.data, "message": "GET callback details", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorised User", "isSuccess": False, "status": 404}, status=200)
