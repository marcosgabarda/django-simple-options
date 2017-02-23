# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import logging
import six
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import IntegrityError

from options.settings import DEFAULT_OPTIONS

logger = logging.getLogger(__name__)


def create_default_options(sender, **kwargs):
    """Creates the defaults configuration options if they don't exists."""
    from options.models import Option
    for key, data in six.iteritems(DEFAULT_OPTIONS):
        if not Option.objects.filter(name=key).exists():
            try:
                Option.objects.create(name=key, **data)
            except IntegrityError:
                logger.warning("Option '%s' already installed" % key)


class ConfigurationsConfig(AppConfig):
    name = "options"

    def ready(self):
        """Connects signals with their managers."""
        post_migrate.connect(create_default_options)
