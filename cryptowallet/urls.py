from django.urls import path, include
from .views import *

urlpatterns = [
    path('balance/check/<str:coin>/', user_crypto_wallet_get_balance_view),
    path('transaction/get/<str:coin>/', user_crypto_wallet_get_transactions_view),
]
