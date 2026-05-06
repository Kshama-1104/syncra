from rest_framework import permissions, viewsets

from .models import MediaAsset
from .serializers import MediaAssetSerializer


class MediaAssetViewSet(viewsets.ModelViewSet):
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MediaAsset.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        uploaded = self.request.FILES["file"]
        serializer.save(owner=self.request.user, content_type=uploaded.content_type, size=uploaded.size)
