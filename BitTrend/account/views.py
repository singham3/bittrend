from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from .serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from datetime import datetime
from django_otp import match_token, devices_for_user, user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
import re
from random import randint
from .emails import _send_account_confirmation_email
from BitTrend.cryptowallet.models import CryptoWallet
from pywallet import wallet
from ..wallet.models import UserWallet


@api_view(['POST'])
def check_email_view(request):
    username_or_email = request.POST.get('username_or_email')
    if User.objects.filter(Q(email=username_or_email) | Q(username=username_or_email)).exists():
        obj = User.objects.filter(Q(email=username_or_email) | Q(username=username_or_email)).first()
        return Response({"data": {'username_or_email': username_or_email, 'is_google_auth': obj.is_google_auth},
                         "message": "Get info", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User not Exists", "isSuccess": False, "status": 404}, status=200)


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    username_or_email = form.cleaned_data['username_or_email']
    password = form.cleaned_data['password']
    otp_token = form.cleaned_data['otp_token']
    user_obj = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
    if user_obj.check_password(password):
        if user_obj.is_email:
            if user_obj.is_google_auth:
                device_match = match_token(user=user_obj, token=otp_token)
                if device_match is None:
                    return Response({"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500}, status=200)
            serializer = TokenObtainPairSerializer(data={'username': user_obj.username, 'password': password})
            token = serializer.validate({'username': user_obj.username, 'password': password})['access']
            user_obj.last_login = datetime.now()
            user_obj.save()
            serializer = AuthUserSerializer(instance=user_obj, many=False).data
            serializer["token"] = token
            serializer['is_kyc'] = True if UserAddress.objects.filter(user=user_obj).exists() and UserDocument.objects.filter(user=user_obj).exists() and UserAddressProof.objects.filter(user=user_obj).exists() else False
            serializer['bank_account'] = True if UserBankAccount.objects.filter(user=user_obj).exists() else False
            data = {'data': serializer, "message": "Successfully Login", "isSuccess": True, "status": 200}
            return Response(data, status=200)
        return Response({"data": None, "message": "Email Is not verified", "isSuccess": False, "status": 500}, status=200)
    else:
        return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(RegisterMiddleware)
def register_view(request, form):
    try:
        serializer = AuthUserSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            seed = wallet.generate_mnemonic()
            for coin in ['eth', 'doge', 'btc', 'btg', 'bch', 'ltc', 'dash', 'qtum']:
                k = wallet.create_wallet(seed=seed, children=0, network=coin)
                CryptoWallet.objects.create(user=user, coin=coin, seed=k['seed'], private_key=k['private_key'],
                                            public_key=k['public_key'], xprivate_key=k['xprivate_key'], xpublic_key=k['xpublic_key'],
                                            wif=k['wif'], xpublic_key_prime=k['xpublic_key_prime'], address=k['address'], network=coin)
            UserWallet(user=user).save()
            input_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
            token_serializer = TokenObtainPairSerializer(data=input_data)
            token = token_serializer.validate(input_data)
            otp = randint(10 ** (6 - 1), (10 ** 6) - 1)
            update_serializer = AuthUserSerializer(instance=user, data={"last_login": datetime.now(), "otp": otp}, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                data = update_serializer.data
                data['token'] = token['access']
                _send_account_confirmation_email(user.id)
                return Response({"data": data, "message": None, "isSuccess": True, "status": 200}, status=200)
            else:
                error = serializer.errors
                error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                return Response({"data": None, "message": error, "isSuccess": True, "status": 500}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500},
                        status=200)


@api_view(['POST', ])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserKYCMiddleware)
def user_kyc_view(request, form):
    error = []
    form.cleaned_data['address']['user'] = request.user.id
    form.cleaned_data['document']['user'] = request.user.id
    form.cleaned_data['address_proof']['user'] = request.user.id
    profile = AuthUserSerializer(instance=request.user, data=form.cleaned_data['profile'], partial=True)
    if profile.is_valid():
        profile.save()
    else:
        err = profile.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        error.append(err)
    if not UserAddress.objects.filter(user=request.user).exists():
        address = UserAddressSerializer(data=form.cleaned_data['address'])
        if address.is_valid():
            address.save()
        else:
            err = address.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            error.append(err)
    if not UserDocument.objects.filter(user=request.user).exists():
        document = UserDocumentSerializer(data=form.cleaned_data['document'])
        if document.is_valid():
            document.save()
        else:
            err = address.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            error.append(err)
    if not UserAddressProof.objects.filter(user=request.user).exists():
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
        return Response({"data": None, "message": "User Profile Updated Successfully", "isSuccess": True, "status": 200}, status=200)


@api_view(['GET', 'POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_google_authentication_view(request):
    def get_user_totp_device(user, confirmed=None):
        if user_has_device(user, confirmed=confirmed):
            device = user.totpdevice_set.get()
            return device
        devices = devices_for_user(user, confirmed=confirmed)
        for device_ in devices:
            if isinstance(device_, TOTPDevice):
                return device_
    try:
        if request.user.is_authenticated:
            if request.user.is_google_auth:
                return Response({"data": None, "message": "Already Activated", "isSuccess": True, "status": 200}, status=200)
            if request.method == 'POST':
                otp_token = request.POST.get('otp_token')
                device_match = match_token(user=request.user, token=otp_token)
                if device_match:
                    request.user.is_google_auth = True
                    request.user.save()
                    return Response({"data": None, "message": "Successfully Activate", "isSuccess": True, "status": 200}, status=200)
                else:
                    return Response({"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500}, status=200)
            else:
                data = {}
                device = get_user_totp_device(request.user, True)
                if not device:
                    device = request.user.totpdevice_set.create(confirmed=True)
                data['qr_code'] = 'https://api.qrserver.com/v1/create-qr-code/?data=' + device.config_url
                data['key'] = re.search('secret=(.*)&algorithm', device.config_url).group(1)
                return Response({"data": data, "message": None, "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_google_authentication_disable_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            otp_token = request.POST.get('otp_token')
            device_match = match_token(user=request.user, token=otp_token)
            if device_match:
                request.user.is_google_auth = False
                request.user.save()
                return Response({"data": None, "message": "Successfully Deactivate", "isSuccess": True, "status": 200}, status=200)
            else:
                return Response({"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', 'PUT'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserBankAccountMiddleware)
def create_or_update_user_bank_account_view(request, id=None, form=None):
    if request.method == "POST":
        form.cleaned_data['user'] = request.user.id
        serializer = UserBankAccountSerializer(data=form.cleaned_data)
    elif request.method == "PUT":
        if id:
            if UserBankAccount.objects.filter(user=request.user, id=id).exists():
                instance = UserBankAccount.objects.get(user=request.user, id=id)
                serializer = UserBankAccountSerializer(data=form.cleaned_data, instance=instance, partial=True)
            else:
                return Response({"data": None, "message": "Account not found", "isSuccess": False, "status": 404}, status=200)
        else:
            return Response({"data": None, "message": "Id is required", "isSuccess": False, "status": 404}, status=200)
    if serializer.is_valid():
        serializer.save()
        serializer = UserBankAccountSerializer(instance=UserBankAccount.objects.filter(user=request.user), many=True)
        return Response({"data": serializer.data, "message": "Bank Account Update Successfully", "isSuccess": True, "status": 200}, status=200)
    else:
        err = serializer.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)


@api_view(['GET', 'DELETE'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def get_or_delete_user_bank_account_view(request, id=None):
    if request.user.is_authenticated:
        if request.method == "DELETE":
            if id:
                if UserBankAccount.objects.filter(user=request.user, id=id).exists():
                    UserBankAccount.objects.get(user=request.user, id=id).delete()
                else:
                    return Response({"data": None, "message": "Account not found", "isSuccess": False, "status": 404}, status=200)
            else:
                return Response({"data": None, "message": "Id is required", "isSuccess": False, "status": 404}, status=200)
        else:
            if id:
                if UserBankAccount.objects.filter(user=request.user, id=id).exists():
                    serializer = UserBankAccountSerializer(instance=UserBankAccount.objects.get(user=request.user, id=id), many=False)
                    return Response({"data": serializer.data, "message": "Bank Account GET Successfully", "isSuccess": True, "status": 200},
                                    status=200)
                else:
                    return Response({"data": None, "message": "Account not found", "isSuccess": False, "status": 404}, status=200)
        serializer = UserBankAccountSerializer(instance=UserBankAccount.objects.filter(user=request.user), many=True)
        return Response({"data": serializer.data, "message": "Bank Account Update Successfully", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(UserProfileMiddleware)
def user_profile_view(request, form=None):
    if request.method == "POST":
        form.cleaned_data['updated_at'] = datetime.now()
        update_serializer = AuthUserSerializer(instance=request.user, data=form.cleaned_data, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response({"data": update_serializer.data, "message": None, "isSuccess": False, "status": 200}, status=200)
        else:
            err = update_serializer.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)
    serializer = AuthUserSerializer(instance=request.user, many=False)
    return Response({"data": serializer.data, "message": None, "isSuccess": False, "status": 200}, status=200)


@api_view(['POST'])
def email_otp_resend_view(request):
    email = request.POST.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        otp = randint(10 ** (6 - 1), (10 ** 6) - 1)
        update_serializer = AuthUserSerializer(instance=user, data={"last_login": datetime.now(), "otp": otp}, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
            _send_account_confirmation_email(user.id)
            return Response({"data": None, "message": "Mail sent successfully", "isSuccess": True, "status": 200}, status=200)
        else:
            err = update_serializer.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "User Not Exists", "isSuccess": False, "status": 404}, status=200)


@api_view(['POST'])
def email_otp_verify_view(request):
    username_or_email = request.POST.get('username_or_email')
    otp = request.POST.get('otp')
    if User.objects.filter(Q(email=username_or_email) | Q(username=username_or_email)).exists():
        if User.objects.filter(Q(email=username_or_email) | Q(username=username_or_email), otp=int(otp)).exists():
            user = User.objects.get(Q(email=username_or_email) | Q(username=username_or_email))
            update_serializer = AuthUserSerializer(instance=user, data={"updated_at": datetime.now(), "otp": None, "is_email": True}, partial=True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({"data": None, "message": "Verified", "isSuccess": True, "status": 200}, status=200)
            else:
                err = update_serializer.errors
                err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
                return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)
        return Response({"data": None, "message": "Incorrect OTP", "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "User Not Exists", "isSuccess": False, "status": 404}, status=200)
