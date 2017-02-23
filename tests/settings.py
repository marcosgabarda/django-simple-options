# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

SECRET_KEY = "dummy"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

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
