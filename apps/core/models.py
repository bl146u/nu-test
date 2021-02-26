from field_history.tracker import FieldHistoryTracker

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from .validators import validate_max_weight_image


UserModel = get_user_model()


class MediaModel(models.Model):
    created = models.DateTimeField("Created", auto_now_add=timezone.now)
    user = models.ForeignKey(
        UserModel, verbose_name="User", on_delete=models.CASCADE, related_name="mdeia",
    )
    image = models.ImageField(
        "Image", upload_to="profile/media", validators=(validate_max_weight_image,)
    )
    history = FieldHistoryTracker(("image",))

    class Meta:
        db_table = "media"
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user} - {self.image}"
