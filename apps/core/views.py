from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, View, FormView, ListView
from django.shortcuts import render

from .forms import AuthForm, LogoutForm, RegistrationForm
from .models import MediaModel


def handler404(request, exception):
    return render(request, "404.html", status=404)


class LoginRequiredMixin(auth_mixins.LoginRequiredMixin):
    login_url = "/auth/"
    redirect_field_name = "destination"


class AlreadyLoginMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"


class FrontView(LoginRequiredMixin, ListView, FormView):
    template_name = "front.html"
    form_class = LogoutForm
    success_url = reverse_lazy("apps_core:auth")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        auth_logout(self.request)
        return super().form_valid(form=form)

    def get_queryset(self):
        return MediaModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        return kwargs


class RegistrationView(AlreadyLoginMixin, auth_views.FormView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("apps_core:front")

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form=form)


class AuthView(auth_views.LoginView):
    template_name = "auth.html"
    redirect_field_name = "destination"
    authentication_form = AuthForm
    redirect_authenticated_user = True
