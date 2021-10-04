from django.utils.deprecation import MiddlewareMixin
from .forms import *
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
import os
import sys


class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            jwt_object = JWTAuthentication()
            header = jwt_object.get_header(request)
            if header is not None:
                raw_token = jwt_object.get_raw_token(header)
                validated_token = jwt_object.get_validated_token(raw_token)
                request.user = jwt_object.get_user(validated_token)
            return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500},
                                status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(data=request.data)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    if "__all__" in error:
                        error = error["__all__"][0]
                    else:
                        error = "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=500)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response(
                {"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500},
                status=200)


class RegisterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = RegisterForm(data=request.data)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    if "__all__" in error:
                        error = error["__all__"][0]
                    else:
                        error = "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=500)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response(
                {"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500},
                status=200)


class UserProfileMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                form = None
                if request.method == "POST":
                    form = UserProfileForm(request.data, request.FILES)
                    if not form.is_valid():
                        error = form.errors
                        if "__all__" in error:
                            error = error["__all__"][0]
                        else:
                            error = "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
                return view_func(request, form)
            return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response(
                {"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500},
                status=200)


class UserKYCMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                if request.method == "POST":
                    form = UserKYCForm(request.data, request.FILES)
                    if form.is_valid():
                        return view_func(request, form)
                    else:
                        error = form.errors
                        if "__all__" in error:
                            error = error["__all__"][0]
                        else:
                            error = "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
            return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response(
                {"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500},
                status=200)


class UserBankAccountMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.method == "POST":
                form = UserBankAccountForm(request.data, request.FILES)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    if "__all__" in error:
                        error = error["__all__"][0]
                    else:
                        error = "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
