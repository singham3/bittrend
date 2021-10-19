from django.db.models import Q
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from django.http import JsonResponse
from .middleware import *
from .serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from datetime import datetime
from django_otp import match_token
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
import re
from cryptowallet.models import CryptoWallet
from pywallet import wallet


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    username_or_email = form.cleaned_data['username_or_email']
    password = form.cleaned_data['password']
    otp_token = form.cleaned_data['otp_token']
    user_obj = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
    if user_obj.check_password(password):
        if user_obj.is_google_auth:
            device_match = match_token(user=user_obj, token=otp_token)
            if device_match is None:
                return Response({"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500},
                                status=200)
        serializer = TokenObtainPairSerializer(data={'username': user_obj.username, 'password': password})
        token = serializer.validate({'username': user_obj.username, 'password': password})['access']
        user_obj.last_login = datetime.now()
        user_obj.save()
        serializer = AuthUserSerializer(instance=user_obj, many=False).data
        serializer["token"] = token
        data = {'data': serializer, "message": "Successfully Login", "isSuccess": True, "status": 200}
        return Response(data, status=200)
    else:
        return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(RegisterMiddleware)
def register_view(request, form):
    serializer = AuthUserSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=form.cleaned_data['username'])
        for coin in ['btc', 'btg', 'bch', 'ltc', 'dash', 'qtum', 'doge']:
            pool = CryptoWallet.objects.filter(coin__icontains=coin, is_pool=True).first()
            user_addr = wallet.create_address(network=coin, xpub=pool.xpublic_key, child=1)
            CryptoWallet.objects.create(user=user, coin=coin, address=user_addr['address']).save()
        input_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
        token_serializer = TokenObtainPairSerializer(data=input_data)
        token = token_serializer.validate(input_data)
        update_serializer = AuthUserSerializer(
            instance=user,
            data={"last_login": datetime.now()},
            partial=True
        )
        if update_serializer.is_valid():
            update_serializer.save()
            data = update_serializer.data
            data['token'] = token['access']
            return Response({"data": data, "message": None, "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            if "__all__" in error:
                error = error["__all__"][0]
            else:
                error = "".join(key + f" {error[key][0]}\n" for key in error)
            return Response({"data": None, "message": error, "isSuccess": True, "status": 500}, status=200)
    else:
        error = serializer.errors
        if "__all__" in error:
            error = error["__all__"][0]
        else:
            error = "".join(key + f" {error[key][0]}\n" for key in error)
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserKYCMiddleware)
def user_kyc_view(request, form):
    error = []
    form.cleaned_data['address']['user'] = request.user.id
    form.cleaned_data['document']['user'] = request.user.id
    form.cleaned_data['address_proof']['user'] = request.user.id
    profile = AuthUserSerializer(instance=User.objects.get(id=request.user.id), data=form.cleaned_data['profile'],
                                 partial=True)
    if profile.is_valid():
        profile.save()
    else:
        err = profile.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    address = UserAddressSerializer(data=form.cleaned_data['address'])
    if address.is_valid():
        address.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    document = UserDocumentSerializer(data=form.cleaned_data['document'])
    if document.is_valid():
        document.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    address_proof = UserAddressProofSerializer(data=form.cleaned_data['address_proof'])
    if address_proof.is_valid():
        address_proof.save()
    else:
        err = address.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    if any(error):
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    else:
        return Response({"data": None, "message": "User Profile Updated Successfully",
                         "isSuccess": True, "status": 200}, status=200)


@api_view(['GET', 'POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_google_authentication_view(request):
    def get_user_totp_device(user, confirmed=None):
        devices = devices_for_user(user, confirmed=confirmed)
        for device in devices:
            if isinstance(device, TOTPDevice):
                return device
    try:
        if request.user.is_authenticated:
            if request.user.is_google_auth:
                return Response({"data": None, "message": "Already Activated", "isSuccess": True, "status": 200},
                                status=200)
            if request.method == 'POST':
                otp_token = request.POST.get('otp_token')
                device_match = match_token(user=request.user, token=otp_token)
                if device_match:
                    request.user.is_google_auth = True
                    request.user.save()
                    return Response({"data": None, "message": "Successfully Activate", "isSuccess": True, "status": 200},
                                    status=200)
                else:
                    return Response(
                        {"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500}, status=200)
            else:
                data = {}
                device = get_user_totp_device(request.user)
                if not device:
                    device = request.user.totpdevice_set.create(confirmed=True)

                    data['qr_code'] = 'https://api.qrserver.com/v1/create-qr-code/?data=' + device.config_url
                    data['key'] = re.search('secret=(.*)&algorithm', device.config_url).group(1)
                return Response({"data": data, "message": None, "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False,
                         "status": 500}, status=200)


@api_view(['POST', ])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserBankAccountMiddleware)
def user_bank_account_view(request, form):
    form.cleaned_data['user'] = request.user.id
    serializer = UserBankAccountSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        accounts = UserBankAccount.objects.filter(user=request.user)
        return Response({"data": UserBankAccountSerializer(instance=accounts, many=True).data,
                         "message": "User Bank Account create Successfully", "isSuccess": True, "status": 200},
                        status=200)
    else:
        err = serializer.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserProfileMiddleware)
def user_profile_view(request, form):
    if request.method == 'POST':
        form.cleaned_data['updated_at'] = datetime.now()
        update_serializer = AuthUserSerializer(
            instance=request.user,
            data=form.cleaned_data,
            partial=True
        )
        if update_serializer.is_valid():
            update_serializer.save()
        else:
            err = update_serializer.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)

    return Response({"data": AuthUserSerializer(instance=request.user, many=False).data,
                     "message": None, "isSuccess": False, "status": 200}, status=200)
