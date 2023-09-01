=====================
Django Simple Options
=====================

.. image:: https://img.shields.io/pypi/v/django-simple-options
    :target: https://pypi.org/project/django-simple-options/
    :alt: PyPI

.. image:: https://codecov.io/gh/marcosgabarda/django-simple-options/branch/main/graph/badge.svg?token=P0XWIJGYZD 
    :target: https://codecov.io/gh/marcosgabarda/django-simple-options

.. image:: https://img.shields.io/badge/code_style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://readthedocs.org/projects/django-simple-options/badge/?version=latest
    :target: https://django-simple-options.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

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

