from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


UserModel = get_user_model()


def validate_unique_email_users(value):
    user_exists = UserModel.objects.filter(email=value).exists()
    if user_exists:
        raise ValidationError("Пользователь с таким E-mail уже существует.")


def validate_max_weight_image(value):
    if value.file.size < settings.MAX_FILE_SIZE:
        raise ValidationError(
            f"Файл не должен превышать {settings.MAX_FILE_SIZE/(1024*1024*1024)} Mb"
        )
