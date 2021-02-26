from django.conf import settings
from django.core.mail import send_mail


def sendmail(subject, message, to):
    if not isinstance(to, list):
        to = [to]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
