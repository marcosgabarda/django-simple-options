=====================
Django Simple Options
=====================

.. image:: https://travis-ci.org/marcosgabarda/django-simple-options.svg?branch=master
    :target: https://travis-ci.org/marcosgabarda/django-simple-options

.. image:: https://coveralls.io/repos/github/marcosgabarda/django-simple-options/badge.svg?branch=master
    :target: https://coveralls.io/github/marcosgabarda/django-simple-options?branch=master


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

