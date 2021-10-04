from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', register_view),
    path('update/', user_profile_view),
    path('get/', user_profile_view),
    path('login/', user_login_view),
    path('kyc/update/', user_kyc_view),
    path('two-step-authentication/active/', user_google_authentication_view),
    path('two-step-authentication/key/get/', user_google_authentication_view),
    path('bank-account/create/', user_bank_account_view)
]
