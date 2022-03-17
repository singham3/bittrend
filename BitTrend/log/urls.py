from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', logs_create_view),
    path('get/', logs_get_view),
]