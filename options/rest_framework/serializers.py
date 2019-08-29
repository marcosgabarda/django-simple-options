from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from options import get_option_model, get_user_option_model
from options.settings import DEFAULT_EXCLUDE_USER

Option = get_option_model()
UserOption = get_user_option_model()


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = [
            "id",
            "name",
            "public_name",
            "type",
            "value",
            "file",
            "is_list",
            "is_public",
        ]


class UserOptionSerializer(OptionSerializer):

    is_public = serializers.BooleanField(default=True, write_only=True)

    class Meta(OptionSerializer.Meta):
        model = UserOption

    def validate_name(self, value):
        """Checks if the name is in DEFAULT_EXCLUDE_USER_OPTIONS."""
        if value in DEFAULT_EXCLUDE_USER:
            raise serializers.ValidationError(
                _("The name in the option can't be handle by the user.")
            )
        return value
