from rangefilter.filter import DateRangeFilter
from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import admin

from .models import MediaModel


class UserFilter(AutocompleteFilter):
    title = "User"
    field_name = "user"


@admin.register(MediaModel)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "created")
    list_filter = (
        UserFilter,
        ("created", DateRangeFilter),
    )
    readonly_fields = ("created",)
    autocomplete_fields = ("user",)

    class Media:
        pass
