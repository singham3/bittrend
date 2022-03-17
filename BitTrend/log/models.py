from django.db import models
from ..account.models import User


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_logs")
    message = models.TextField(max_length=65500)
    device_name = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
