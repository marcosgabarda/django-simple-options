from django.contrib import admin

from options.models import Option, UserOption


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Manage configuration options."""

    list_display = ["public_name", "value", "is_public"]
    list_filter = ["is_public"]
    search_fields = ["public_name", "name"]


@admin.register(UserOption)
class UserOptionAdmin(admin.ModelAdmin):
    """Manage configuration user options."""

    list_display = ["user", "public_name", "value", "is_public"]
    list_filter = ["is_public"]
    search_fields = ["public_name", "name"]
