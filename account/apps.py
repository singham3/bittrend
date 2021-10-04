from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'


def create_superuser_user(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    from cryptowallet.models import CryptoWallet
    from pywallet import wallet

    user = get_user_model()
    manager = user.objects
    try:
        manager.get(username="admin")
    except user.DoesNotExist:
        manager.create_superuser(username="admin", email="admin@bittrend.io", password='Admin&9876543210')
    superuser = manager.get(username="admin", is_superuser=True)
    for coin in ['btc', 'btg', 'bch', 'ltc', 'dash', 'qtum', 'doge']:
        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network=coin, seed=seed, children=0)
        CryptoWallet.objects.create(
            user=superuser,
            coin=w['coin'],
            seed=w['seed'],
            private_key=w['private_key'],
            public_key=w['public_key'],
            xprivate_key=w['xprivate_key'],
            xpublic_key=w['xpublic_key'],
            wif=w['wif'],
            xpublic_key_prime=w['xpublic_key_prime'],
            address=w['address'],
            is_pool=True
        )


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_superuser_user)
