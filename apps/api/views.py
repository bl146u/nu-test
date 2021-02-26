from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.core import models as core_models
from apps.core import serializers as core_serializers
from apps.core import utils as core_utils
from .serializers import UploadImageSerializer, UpdateImageSerializer


class UploadImageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST,)

        image_instance = core_models.MediaModel.objects.create(
            user=self.request.user, image=serializer.validated_data.get("data")
        )
        image = core_serializers.UserImageSerializer(instance=image_instance)

        message = [
            str(self.request.user),
            image.data.get("created"),
            image.data.get("image"),
        ]
        core_utils.sendmail(
            "Изображение загружено", ";".join(message), self.request.user.email
        )

        return Response(image.data, status=HTTP_200_OK)


class UpdateImageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UpdateImageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        image_instance = core_models.MediaModel.objects.filter(
            user=self.request.user, id=serializer.validated_data.get("id")
        ).first()
        if not image_instance:
            return Response(
                {"error": "Неверный данные для обновления изображения"},
                status=HTTP_400_BAD_REQUEST,
            )

        image_instance.image = serializer.validated_data.get("data")
        image_instance.save()

        image = core_serializers.UserImageSerializer(instance=image_instance)

        message = [
            str(self.request.user),
            image.data.get("history")[-1].get("created"),
            image.data.get("image"),
        ]

        core_utils.sendmail(
            "Изображение обновлено", ";".join(message), self.request.user.email
        )

        return Response(image.data, status=HTTP_200_OK)
