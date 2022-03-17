from django.contrib.auth.tokens import default_token_generator
from templated_email import send_templated_mail
from urllib.parse import urlparse, urlsplit, urlencode
from .models import User
from django.conf import settings
from django.core.mail import send_mail


def get_email_context(id):
    user = User.objects.get(id=id)
    return {
        "template_name": "account/confirm",
        "from_email": "srishtip0704@gmail.com",
        "recipient_list": [user.email],
        "context": {
            'username': user.id,
            'full_name': user.get_full_name(),
            'signup_date': user.date_joined,
            'otp': user.otp,
        },
    }


def _send_account_confirmation_email(id):
    context = get_email_context(id)
    send_templated_mail(**context)
