from rest_framework import serializers

from .models import MediaAsset


class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = ("id", "owner", "file", "content_type", "size", "created_at")
        read_only_fields = ("owner", "content_type", "size")

    def validate_file(self, file):
        max_size = 10 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError("File must be 10MB or smaller.")
        return file
