from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


class UploadImageSerializer(serializers.Serializer):
    data = Base64ImageField()


class UpdateImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data = Base64ImageField()
