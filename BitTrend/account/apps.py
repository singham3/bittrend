from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BitTrend.account'


def create_superuser_user(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    from ..cryptowallet.models import CryptoWallet, TestCryptoWallet
    from django.conf import settings
    user = get_user_model()
    manager = user.objects
    try:
        obj = manager.get(username="admin")
    except user.DoesNotExist:
        obj = manager.create_superuser(username="admin", email="admin@bittrend.io", password='Admin&9876543210')
        coins = settings.CLIENT.coin_info()
        for i in coins:
            try:
                network_address = [
                    {'network': n['network'],
                     'address': settings.CLIENT.deposit_address(coin=i['coin'], network=n['network'])['address']} for n in i['networkList']
                ]
                if not CryptoWallet.objects.filter(user=obj, coin=i['coin']).exists():
                    CryptoWallet(user=manager.get(username="admin"), coin=i['coin'], network_address=str(network_address), is_pool=True).save()
            except Exception as e:
                continue
        for i in settings.TEST_CLIENT.account()['balances']:
            if TestCryptoWallet.objects.filter(user=obj, coin=i['asset']).exists():
                TestCryptoWallet.objects.filter(user=obj, coin=i['asset']).update(balance=i['free'], locked=i['locked'])
            else:
                TestCryptoWallet.objects.create(user=obj, coin=i['asset'], balance=i['free'], locked=i['locked'], is_pool=True)


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_superuser_user)
