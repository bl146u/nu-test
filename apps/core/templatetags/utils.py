from django import template
from django.utils import timezone


register = template.Library()


@register.simple_tag
def date_format(value):
    return timezone.localtime(value).strftime("%d.%m.%Y %H:%M:%S")
