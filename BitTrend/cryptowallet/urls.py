from django.urls import path, include
from .views import *

urlpatterns = [
    path('balance/check/', user_crypto_wallet_get_balance_view),
    path('balance/check/<str:coin>/', user_crypto_wallet_get_balance_view),
    path('test/balance/check/', user_test_crypto_wallet_get_balance_view),
    path('test/order/get/<str:symbol>/', user_crypto_wallet_get_test_order_view),
    path('test/order/create/', user_crypto_wallet_create_test_order_view),
    path('test/order/cancel/', user_crypto_wallet_cancel_test_order_view),
    path('get/', user_crypto_wallet_get_view),
    path('admin/get/', admin_crypto_wallet_get_view),
    path('admin/get/<str:coin>/', admin_crypto_wallet_get_view),
    path('mainnet/order-details/<str:mode>/<str:symbol>/', user_crypto_wallet_get_mainnet_order_view),
    path('order/create/', user_crypto_wallet_create_new_order_view),
    path('order/cancel/', user_crypto_wallet_cancel_mainnet_order_view),
    path('price-calculator/<str:symbol>/', crypto_price_calculator),
    path('withdrawal/history/', withdrawal_history),
    path('deposit/history/', deposit_history),
]
