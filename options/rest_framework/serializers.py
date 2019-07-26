from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from options.settings import DEFAULT_EXCLUDE_USER_OPTIONS
from options.models import Option, UserOption


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "name", "public_name", "type", "value", "is_list"]


class UserOptionSerializer(OptionSerializer):
    class Meta(OptionSerializer.Meta):
        model = UserOption

    def validate_name(self, value):
        """Checks if the name is in DEFAULT_EXCLUDE_USER_OPTIONS."""
        if value in DEFAULT_EXCLUDE_USER_OPTIONS:
            raise serializers.ValidationError(
                _("The name in the option can't be handle by the user.")
            )
