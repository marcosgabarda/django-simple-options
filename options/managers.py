from threading import local
from typing import TYPE_CHECKING, Optional, Sequence, Union

from django.db import models

from options import get_option_model
from options.settings import DEFAULT_EXCLUDE_USER

if TYPE_CHECKING:
    from django.contrib.auth.models import User

_active = local()  # Active thread


class OptionQuerySet(models.QuerySet):
    def public(self) -> "OptionQuerySet":
        """Gets public options."""
        return self.filter(is_public=True)


class OptionManager(models.Manager):
    """Manager for options."""

    cache_prefix = "_options_option_"

    def __get_cached_value(
        self, name: str
    ) -> Optional[Union[int, float, str, Sequence]]:
        return getattr(_active, f"{self.cache_prefix}{name}", None)

    def __set_cached_value(
        self, name: str, value: Union[int, float, str, Sequence]
    ) -> None:
        return setattr(_active, f"{self.cache_prefix}{name}", value)

    def get_queryset(self) -> "OptionQuerySet":
        return OptionQuerySet(self.model, using=self._db)

    def public(self) -> "OptionQuerySet":
        """Gets public options."""
        return self.get_queryset().public()

    def get_value(
        self, name: str, default: Optional[Union[int, float, str, Sequence]] = None
    ) -> Optional[Union[int, float, str, Sequence]]:
        """Gets the value with the proper type."""
        _cached_value = self.__get_cached_value(name=name)
        if _cached_value is not None:
            return _cached_value
        try:
            option = self.model.objects.get(name=name)
            value = option.get_value()
        except self.model.DoesNotExist:
            value = default
        self.__set_cached_value(name=name, value=value)
        return value


class UserOptionQuerySet(models.QuerySet):
    def public(self) -> "UserOptionQuerySet":
        """Gets public options."""
        return self.filter(is_public=True)


class UserOptionManager(models.Manager):
    """Manager to handle user's custom options."""

    cache_prefix = "_option_user_option_"

    def __get_cached_value(
        self, name: str, user: Optional["User"] = None
    ) -> Optional[Union[int, float, str, Sequence]]:
        key = (
            f"{self.cache_prefix}{name}"
            if user is None
            else f"{self.cache_prefix}{name}_{user.pk}"
        )
        return getattr(_active, key, None)

    def __set_cached_value(
        self,
        name: str,
        value: Union[int, float, str, Sequence],
        user: Optional["User"] = None,
    ) -> None:
        key = (
            f"{self.cache_prefix}{name}"
            if user is None
            else f"{self.cache_prefix}{name}_{user.pk}"
        )
        return setattr(_active, key, value)

    def get_queryset(self) -> "UserOptionQuerySet":
        return OptionQuerySet(self.model, using=self._db)

    def public(self) -> "UserOptionQuerySet":
        """Gets public options."""
        return self.get_queryset().public()

    def filter_user_customizable(self) -> "UserOptionQuerySet":
        """Returns option that the user can customize himself."""
        return self.exclude(name__in=DEFAULT_EXCLUDE_USER)

    def get_value(
        self,
        name,
        user: Optional["User"] = None,
        default: Optional[Union[int, float, str, Sequence]] = None,
    ) -> Optional[Union[int, float, str, Sequence]]:
        """Gets the value with the proper type."""
        Option = get_option_model()
        _cached_value = self.__get_cached_value(name=name, user=user)
        if _cached_value is not None:
            return _cached_value
        if user is None:
            value = Option.objects.get_value(name=name, default=default)
        try:
            option = self.model.objects.get(user=user, name=name)
            value = option.get_value()
        except self.model.DoesNotExist:
            value = Option.objects.get_value(name=name, default=default)
        self.__set_cached_value(name=name, value=value, user=user)
        return value
