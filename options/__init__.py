"""Simple app to add configuration options to a Django project."""
import django

from options.constants import CONVERTER, FILE, FLOAT, INT, STR, TYPE_CHOICES
from options.helpers import get_option_model, get_user_option_model

__all__ = [
    "get_option_model",
    "get_user_option_model",
    "FLOAT",
    "INT",
    "STR",
    "FILE",
    "TYPE_CHOICES",
    "CONVERTER",
]
__version__ = "2.4.0"

if django.VERSION < (3, 2):
    default_app_config = "options.apps.ConfigurationsConfig"
