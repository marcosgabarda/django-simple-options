# -*- coding: utf-8 -*-


import six
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from options import STRING, TYPE_CHOICES, INT, FLOAT
from options.managers import OptionManager, UserOptionManager


class BaseOption(models.Model):
    """Base model for system options and configurations."""

    name = models.CharField(
        verbose_name=_("Parameter"), max_length=255, unique=True, db_index=True
    )
    public_name = models.CharField(
        verbose_name=_("Public name of the parameter"),
        max_length=255,
        unique=False,
        db_index=True,
    )
    type = models.PositiveIntegerField(choices=TYPE_CHOICES, default=STRING)
    value = models.CharField(
        null=True, blank=True, default=None, max_length=256, verbose_name=_("Value")
    )
    is_list = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s" % self.public_name

    def _convert_value(self, value, type):
        converter = {INT: int, FLOAT: float, STRING: six.text_type}
        default_values = {INT: 0, FLOAT: 1.0, STRING: ""}
        try:
            option_value = converter.get(self.type, six.text_type)(self.value)
        except ValueError:
            option_value = default_values.get(self.type)
        return option_value

    def get_value(self):
        """Gets the value with the proper type. If the type is not
        valid it would return the default value for the field, to avoid
        problems with manual database modifications"""

        if not self.is_list:
            return self._convert_value(self.value, self.type)
        else:
            values = self.value.split(",")
            return [self._convert_value(self.type, item) for item in values]

    def clean(self):
        from django.core.exceptions import ValidationError

        converter = {INT: int, FLOAT: float, STRING: six.text_type}
        try:
            converter.get(self.type, six.text_type)(self.value)
        except ValueError:
            raise ValidationError(_("Invalid value for this type."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Option(BaseOption):
    """System options and configurations."""

    objects = OptionManager()

    class Meta:
        ordering = ["public_name"]


class UserOption(BaseOption):
    """Custom option for a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="options", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Parameter"), max_length=255)

    objects = UserOptionManager()

    class Meta:
        unique_together = ["user", "name"]
        ordering = ["public_name"]
