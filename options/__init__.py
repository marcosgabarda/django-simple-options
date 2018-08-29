# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django import get_version
from django.utils.translation import ugettext_lazy as _


FLOAT, INT, STRING = (0, 1, 2)
TYPE_CHOICES = (
    (FLOAT, _("Float")),
    (INT, _("Integer")),
    (STRING, _("String")),
)

default_app_config = 'options.apps.ConfigurationsConfig'

VERSION = (1, 0, 0, 'alpha', 3)

__version__ = get_version(VERSION)
