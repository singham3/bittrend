from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from .serializer import *
from ..account.middleware import TokenAuthenticationMiddleware


@api_view(['POST', 'GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(GalleryMiddleware)
def image_upload_view(request, form=None, id=None):
    if request.method == "POST":
        serializer = GallerySerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "File Uploaded", "isSuccess": True, "status": 200}, status=200)
        else:
            err = serializer.errors
            err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
            return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)
    if id and Gallery.objects.filter(id=id).exists():
        serializer = GallerySerializer(instance=Gallery.objects.get(id=id))
        return Response({"data": serializer.data, "message": "File Uploaded", "isSuccess": True, "status": 200}, status=200)
    else:
        return Response({"data": None, "message": "valid id required", "isSuccess": True, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def bulk_image_upload_view(request):
    if request.method == "POST":
        if 'images' in request.FILES:
            files = [{"image": i} for i in request.FILES.getlist('images')]
            serializer = GallerySerializer(data=files, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "message": "Files Uploaded", "isSuccess": True, "status": 200}, status=200)
            else:
                err = serializer.errors
                err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
                return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)
        elif "ids" in request.POST:
            ids = Gallery.objects.filter(ids__in=eval(request.POST.get('ids')))
            serializer = GallerySerializer(instance=ids, many=True)
            return Response({"data": serializer.data, "message": "Files Get Successfully", "isSuccess": True, "status": 200}, status=200)
