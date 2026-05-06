from django.conf import settings
from django.db import models


class MediaAsset(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="media_assets")
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    content_type = models.CharField(max_length=120)
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "-created_at"])]
