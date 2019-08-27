import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from options import get_option_model
from options.settings import DEFAULT_CONFIGURATION

logger = logging.getLogger(__name__)


def create_default_options(sender, **kwargs):
    """Creates the defaults configuration options if they don't exists."""
    Option = get_option_model()

    for key, data in DEFAULT_CONFIGURATION.items():
        if not Option.objects.filter(name=key).exists():
            try:
                Option.objects.create(name=key, **data)
            except IntegrityError:
                logger.warning("Option '%s' already installed" % key)


class ConfigurationsConfig(AppConfig):
    name = "options"
    verbose_name = _("Options")

    def ready(self):
        """Connects signals with their managers."""
        post_migrate.connect(create_default_options)
