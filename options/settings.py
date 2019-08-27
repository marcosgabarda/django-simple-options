from django.conf import settings

# Needed to build and publish with Flit
# ------------------------------------------------------------------------------
SECRET_KEY = "snitch"

# Specific project configuration
# ------------------------------------------------------------------------------
# Set on settings the default options for this project. These will be created
# on the post migrate signal handler.
# Sample:
#
# SIMPLE_OPTIONS_CONFIGURATION = {
#     "sold_out": {
#         "value": 0,
#         "type": INT,
#         "public_name": "Sets tickets as sold out"
#     },
# }
#
DEFAULT_CONFIGURATION = getattr(settings, "SIMPLE_OPTIONS_CONFIGURATION", {})

# Set the list of options that the user can't customize.
DEFAULT_EXCLUDE_USER = getattr(settings, "SIMPLE_OPTIONS_EXCLUDE_USER", tuple())

# Swappable Option model
DEFAULT_OPTION_MODEL = getattr(
    settings, "SIMPLE_OPTIONS_OPTION_MODEL", "options.Option"
)

# Swappable UserOption model
DEFAULT_USER_OPTION_MODEL = getattr(
    settings, "SIMPLE_OPTIONS_USER_OPTION_MODEL", "options.UserOption"
)
