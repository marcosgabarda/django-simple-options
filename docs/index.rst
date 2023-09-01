.. Django Belt documentation master file, created by
   sphinx-quickstart on Wed Feb  5 10:19:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================
Django Simple Options's documentation
=====================================

Simple app to add configuration options to a Django project.

Quick start
-----------

**1** Install using pip::

    $ pip install django-simple-options

**2** Add "options" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS += ('options',)


Settings options
----------------

Use ``SIMPLE_OPTIONS_CONFIGURATION_DEFAULT`` to set the default options::

    SIMPLE_OPTIONS_CONFIGURATION_DEFAULT = {
        "sold_out": {
            "value": 0,
            "type": INT,
            "public_name": "Sets tickets as sold out"
        },
    }

