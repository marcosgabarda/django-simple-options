from django.db import models

from options import get_option_model
from options.settings import DEFAULT_EXCLUDE_USER


class OptionQuerySet(models.QuerySet):
    def public(self):
        """Gets public options."""
        return self.filter(is_public=True)


class OptionManager(models.Manager):
    """Manager for options."""

    def get_queryset(self):
        return OptionQuerySet(self.model, using=self._db)

    def public(self):
        """Gets public options."""
        return self.get_queryset().public()

    def get_value(self, name, default=None):
        """Gets the value with the proper type."""
        try:
            option = self.model.objects.get(name=name)
            return option.get_value()
        except self.model.DoesNotExist:
            return default


class UserOptionQuerySet(models.QuerySet):
    def public(self):
        """Gets public options."""
        return self.filter(is_public=True)


class UserOptionManager(models.Manager):
    """Manager to handle user's custom options."""

    def get_queryset(self):
        return OptionQuerySet(self.model, using=self._db)

    def public(self):
        """Gets public options."""
        return self.get_queryset().public()

    def filter_user_customizable(self):
        """Returns option that the user can customize himself."""
        return self.exclude(name__in=DEFAULT_EXCLUDE_USER)

    def get_value(self, name, user=None, default=None):
        """Gets the value with the proper type."""
        Option = get_option_model()

        if user is None:
            return Option.objects.get_value(name=name, default=default)
        try:
            option = self.model.objects.get(user=user, name=name)
            return option.get_value()
        except self.model.DoesNotExist:
            return Option.objects.get_value(name=name, default=default)
