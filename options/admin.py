from django.contrib import admin
from options.models import Option


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Manage configuration options."""

    list_display = ["public_name", "value"]
    search_fields = ["public_name", "name"]
