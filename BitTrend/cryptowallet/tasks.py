from ..celery import app
from .models import Order, CryptoWallet
from django.conf import settings


@app.task()
def crypto_order_check_task():
    for i in Order.objects.exclude(status='Filing'):
        response = settings.CLIENT.get_order(i.symbol, orderId=i.orderId)
        if response:
            if response['status'] == 'Filing':
                address = CryptoWallet.objects.filter(user=i.user, coin=i.symbol)
                settings.CLIENT.withdraw(coin=i.symbol, amount=i.origQty, address=address.address)
            i.update(**response)


