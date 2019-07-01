# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from django.conf import settings


# Set on settings the default options for this project. These will be created
# on the post migrate signal handler.
# Sample:
#
# CONFIGURATION_DEFAULT_OPTIONS = {
#     "sold_out": {
#         "value": 0,
#         "type": INT,
#         "public_name": "Sets tickets as sold out"
#     },
# }
#
DEFAULT_OPTIONS = getattr(settings, "CONFIGURATION_DEFAULT_OPTIONS", {})

# Set the list of options that the user can't customize.
DEFAULT_EXCLUDE_USER_OPTIONS = getattr(settings, "EXCLUDE_USER_OPTIONS", tuple())