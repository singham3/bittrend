from django.utils.deprecation import MiddlewareMixin
from .forms import *
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
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
        except InvalidToken as e:
            return Response({'data': None, "message": f"{e.detail.get('detail')}", "status": 500}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({'data': None, "message": f"{e, f_name}, {exc_tb.tb_lineno}", "status": 500}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = UserLoginForm(data=request.data)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=500)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)


class RegisterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.method == "POST":
                form = RegisterForm(data=request.data)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=500)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
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
                        error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
                return view_func(request, form)
            return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)


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
                        error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
            return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)


class UserBankAccountMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            form = None
            id = view_kwargs['id'] if 'id' in view_kwargs and view_kwargs['id'] else None
            if request.method in ("POST", 'PUT'):
                form = UserBankAccountForm(request.data, request.FILES)
                if not form.is_valid():
                    error = form.errors
                    error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
            return view_func(request, id, form)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
