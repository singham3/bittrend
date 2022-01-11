from django.urls import path, include
from .views import *

urlpatterns = [
    path('upload/', image_upload_view),
    path('bulk/upload/', bulk_image_upload_view),
    path('bulk/get/', bulk_image_upload_view),
    path('get/<int:id>/', image_upload_view),
]
