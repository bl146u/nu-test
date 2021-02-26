from django.urls import path

from . import views as api_views


app_name = "apps_api"

urlpatterns = [
    path("upload-image/", api_views.UploadImageAPIView.as_view(), name="upload_image"),
    path("update-image/", api_views.UpdateImageAPIView.as_view(), name="update_image"),
]
