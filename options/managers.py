from django.db import models
from options.settings import DEFAULT_EXCLUDE_USER_OPTIONS


class OptionManager(models.Manager):
    """Manager for options."""

    def get_value(self, name, default=None):
        """Gets the value with the proper type."""
        try:
            option = self.model.objects.get(name=name)
            return option.get_value()
        except self.model.DoesNotExist:
            return default


class UserOptionManager(models.Manager):
    """Manager to handle user's custom options."""

    def filter_user_customizable(self):
        """Returns option that the user can customize himself."""
        return self.exclude(name__in=DEFAULT_EXCLUDE_USER_OPTIONS)

    def get_value(self, name, user=None, default=None):
        """Gets the value with the proper type."""
        from options.models import Option

        if user is None:
            return Option.objects.get_value(name=name, default=default)
        try:
            option = self.model.objects.get(user=user, name=name)
            return option.get_value()
        except self.model.DoesNotExist:
            return Option.objects.get_value(name=name, default=default)
