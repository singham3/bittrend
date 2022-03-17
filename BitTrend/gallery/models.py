from django.db import models


class Gallery(models.Model):
    image = models.FileField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)
