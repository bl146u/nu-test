from crispy_forms import helper, layout

from django import forms
from django.urls import reverse
from django.contrib.auth import forms as auth_forms

from .validators import validate_unique_email_users


class AuthForm(auth_forms.AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

        self.helper = helper.FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = reverse("apps_core:auth")
        self.helper.attrs.update({"novalidate": "novalidate"})

        self.helper.layout = layout.Layout(
            "username",
            "password",
            layout.ButtonHolder(layout.Submit("submit", "Войти")),
        )


class LogoutForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = helper.FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = reverse("apps_core:front")
        self.helper.attrs.update({"novalidate": "novalidate"})

        self.helper.layout = layout.Layout(
            layout.ButtonHolder(layout.Submit("submit", "Выйти"),),
        )


class RegistrationForm(auth_forms.UserCreationForm):
    email = forms.EmailField(validators=(validate_unique_email_users,))

    class Meta(auth_forms.UserCreationForm.Meta):
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = helper.FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = reverse("apps_core:registration")
        self.helper.attrs.update({"novalidate": "novalidate"})

        self.helper.layout = layout.Layout(
            "username",
            "email",
            "password1",
            "password2",
            layout.ButtonHolder(layout.Submit("submit", "Зарегистрироваться")),
        )
