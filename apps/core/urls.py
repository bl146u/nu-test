from django.urls import path

from . import views as core_views


app_name = "apps_core"

urlpatterns = [
    path("robots.txt", core_views.RobotsView.as_view(), name="robots"),
    path("auth/", core_views.AuthView.as_view(), name="auth"),
    path("registration/", core_views.RegistrationView.as_view(), name="registration"),
    path("", core_views.FrontView.as_view(), name="front"),
]
