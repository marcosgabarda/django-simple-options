import six
from django import get_version
from django.utils.translation import ugettext_lazy as _


FLOAT, INT, STRING = (0, 1, 2)
TYPE_CHOICES = ((FLOAT, _("Float")), (INT, _("Integer")), (STRING, _("String")))
CONVERTER = {INT: int, FLOAT: float, STRING: six.text_type}

default_app_config = "options.apps.ConfigurationsConfig"

VERSION = (1, 2, 0, "final", 0)

__version__ = get_version(VERSION)
