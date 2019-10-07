import django

DEBUG = True
USE_TZ = True

SECRET_KEY = "dummy"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "options",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

INSTALLED_APPS += ("rest_framework", "rest_framework.authtoken")
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}
from options.constants import STR

SIMPLE_OPTIONS_CONFIGURATION = {
    "default_option": {
        "public_name": "Default Option",
        "type": STR,
        "value": "default",
    }
}
SIMPLE_OPTIONS_EXCLUDE_USER = ["secret_option"]
