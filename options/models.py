# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import six
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from options import STRING, TYPE_CHOICES, INT, FLOAT
from options.managers import OptionManager, UserOptionManager

@python_2_unicode_compatible
class BaseOption(models.Model):
    """Base model for system options and configurations."""

    name = models.CharField(
        verbose_name=_("Parameter"),
        max_length=255,
        unique=True,
        db_index=True
    )
    public_name = models.CharField(
        verbose_name=_("Public name of the parameter"),
        max_length=255,
        unique=False,
        db_index=True
    )
    type = models.PositiveIntegerField(
        choices=TYPE_CHOICES,
        default=STRING
    )
    value = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=256,
        verbose_name=_("Value")
    )
    is_list = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s" % self.public_name

    def get_value(self):
        """Gets the value with the proper type."""
        converter = {
            INT: int,
            FLOAT: float,
            STRING: six.text_type
        }
        if not self.is_list:
            return converter.get(self.type, six.text_type)(self.value)
        else:
            values = self.value.split(",")
            return list(map(lambda item: converter.get(self.type, six.text_type)(item), values))



class Option(BaseOption):
    """System options and configurations."""

    objects = OptionManager()

    class Meta:
        ordering = ["public_name"]



class UserOption(BaseOption):
    """Custom option for a user."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="options", on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_("Parameter"),
        max_length=255,
    )

    objects = UserOptionManager()

    class Meta:
        unique_together = ["user", "name"]
        ordering = ["public_name"]
