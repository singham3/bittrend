from django.utils.deprecation import MiddlewareMixin
from .forms import *
from rest_framework.response import Response
import os
import sys


class CreateTestOrderMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                form = CreateTestOrderForm(request.data, request.FILES)
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


class CancelTestOrderMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                form = CancelTestOrderForm(request.data, request.FILES)
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


class CryptoPriceCalculatorMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            symbol = view_kwargs['symbol'] if 'symbol' in view_kwargs and view_kwargs['symbol'] else None
            form = CryptoPriceCalculatorForm(request.data, request.FILES)
            if not form.is_valid():
                error = form.errors
                error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
            return view_func(request, symbol, form)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return Response({"data": None, "message": f"{e, exc_type, fname, exc_tb.tb_lineno}", "isSuccess": False, "status": 500}, status=200)
