from django.urls import path
from .views import *

urlpatterns = [
    path('test/payment/generate/', test_paypal_payment_create_view),
    path('test/payment/return/', test_paypal_payment_return_view),
    path('test/payment/cancel/', test_paypal_payment_cancel_view),
    path('test/payment/get/', test_paypal_payment_get_all_view),
    path('test/payment/get/<int:id>/', test_paypal_payment_get_view),
    path('test/payment/get/<str:paymentId>/', test_paypal_payment_get_view),
    path('wallet/get/', user_wallet_get_view),
]
