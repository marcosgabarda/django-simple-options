.. :changelog:

History
-------

2.4.0 (2023-09-04)
++++++++++++++++++

* Chore: Update dependencies, added GitHub Actions and docs.

2.3.1 (2022-08-09)
++++++++++++++++++

* Feat: Changed thread cache with Django cache

2.3.0 (2022-08-03)
++++++++++++++++++

* Feat: Added thread cache
* Feat: Added help text for option
* Feat: Added typing

2.2.1 (2022-06-17)
++++++++++++++++++

* Fix: Optional default_app_config

2.2.0 (2022-06-17)
++++++++++++++++++

* Feat: Support for Django 4.0.
* Fix: Better format in code.

2.1.2 (2020-07-13)
++++++++++++++++++

* Fixed problem with lists (Thanks to @saruba!)

2.1.1 (2019-09-20)
++++++++++++++++++

* Changed STRING to STR (Thanks to @seik!)

2.1.0 (2019-08-29)
++++++++++++++++++

* Added public option to Option.
* Changed permissions classes to OptionViewSet.


2.0.2 (2019-08-27)
++++++++++++++++++

* Changed admin module.

2.0.1 (2019-08-27)
++++++++++++++++++

* Fixed bug with import settings.

2.0 (2019-08-27)
++++++++++++++++

* Drop support for Python 2.
* ``Option`` model and ``UserOption`` model are now swappable.
* Added option for file options.
* Changed names of settings variables.
* Added ``pyptoject.toml`` to distribute.
* Tests running with pytest.

1.2 (2019-07-26)
+++++++++++++++++

* Added admin to user options.
* Added integration with Django Rest Framework.
* Added tests.

1.1 (2019-07-01)
+++++++++++++++++

* Added validation on types before saving (Thanks to @aaloy!).

1.0 (2018-10-2)
+++++++++++++++++

* Added model for user's custom options.

1.0a3 (2018-8-29)
+++++++++++++++++

* Fixed dependency with GeoDejango.

1.0a2 (2017-2-20)
+++++++++++++++++

* Add search options to admin.
* Export current options command.

1.0a1 (2017-2-20)
+++++++++++++++++

* First release on PyPI.
