from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from BitTrend.account.middleware import TokenAuthenticationMiddleware
from .serializer import LogsSerializer
from .middleware import LogsMiddleware
from rest_framework.response import Response
from .models import Logs


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(LogsMiddleware)
def logs_create_view(request, form):
    form.cleaned_data['user'] = request.user.id
    serializer = LogsSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data, "message": "Successfully log created", "isSuccess": True, "status": 200}, status=200)
    else:
        err = serializer.errors
        err = err["__all__"][0] if "__all__" in err else "".join(key + f" {err[key][0]}\n" for key in err)
        return Response({"data": None, "message": err, "isSuccess": False, "status": 500}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def logs_get_view(request):
    if request.user.is_authenticated:
        serializer = LogsSerializer(instance=Logs.objects.filter(user=request.user), many=True)
        return Response({"data": serializer.data, "message": "Successfully log created", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User Not Login", "isSuccess": False, "status": 500}, status=200)

