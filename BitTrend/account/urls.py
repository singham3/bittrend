from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', register_view),
    path('check/', check_email_view),
    path('update/', user_profile_view),
    path('get/', user_profile_view),
    path('login/', user_login_view),
    path('kyc/update/', user_kyc_view),
    path('two-step-authentication/active/', user_google_authentication_view),
    path('two-step-authentication/deactivate/', user_google_authentication_disable_view),
    path('two-step-authentication/key/get/', user_google_authentication_view),
    path('bank-account/create/', create_or_update_user_bank_account_view),
    path('bank-account/edit/<int:id>/', create_or_update_user_bank_account_view),
    path('bank-account/get/', get_or_delete_user_bank_account_view),
    path('bank-account/get/<int:id>/', get_or_delete_user_bank_account_view),
    path('bank-account/delete/<int:id>/', get_or_delete_user_bank_account_view),
    path('email/otp/verify/', email_otp_verify_view),
    path('email/otp/resend/', email_otp_resend_view)
]
