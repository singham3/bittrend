from django.utils.deprecation import MiddlewareMixin
from .forms import *
from rest_framework.response import Response


class GalleryMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            id = view_args['id'] if 'id' in view_args and view_args['id'] else None
            if request.method == "POST":
                form = GalleryForm(request.data, request.FILES)
                if form.is_valid():
                    return view_func(request, form)
                else:
                    error = form.errors
                    error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                    return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
            return view_func(request, None, id)
        return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)
