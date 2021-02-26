from field_history.models import FieldHistory
from rest_framework import serializers

from django.utils import timezone

from .models import MediaModel


class ImageHistorySerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = FieldHistory
        fields = ("created", "image")

    def get_created(self, instance):
        return timezone.localtime(instance.date_created).strftime("%d.%m.%Y %H:%M:%S")

    def get_image(self, instance):
        return str(instance.field_value)


class UserImageSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    history = ImageHistorySerializer(many=True)

    class Meta:
        model = MediaModel
        fields = ("id", "created", "image", "history")

    def get_created(self, instance):
        return timezone.localtime(instance.created).strftime("%d.%m.%Y %H:%M:%S")

    def get_image(self, instance):
        return instance.image.url
