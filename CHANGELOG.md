Change Log
==========


4.0.0
-----

* Upgraded to Django 6.1.
* Removed support for Django 4.2.
* Removed support for Python 3.8 - 3.10.
* Added support for Python 3.12 - 3.14.
* Replaced setup.py, tox.ini, and requirements with pyproject.toml.
* Replaced flake8 with ruff for linting.
* Bundled the xlink and xml XSD schemas with the tests so schema validation
  no longer fetches remote files (lxml 6 can no longer load schemas over HTTP).


3.0.0
-----

* Upgraded to Django 4.2.


2.0.0
-----

* Upgraded to Django 4.1.
* Removed support for Django 2.2.
* Removed support for Python 3.6 and 3.7.
* Added support for Python 3.10.


1.0.0
-----

* Upgraded to Django 2.2.
* Removed support for Django 1.11 and versions below.
* Removed support for Python 2.7.
* Replaced Travis with Github Actions.
* Added Python 3.8 and 3.9 to testing.
* Removed Python 3.5 from testing.


0.1.2
-----

* Expanded tests to cover more Python and Django versions.
* Expanded stated Django and Python compatibility.
* Changed string definition of max_length for charfield to an integer.
* Now works on Django 1.11


0.1.1
-----

* Added CHANGELOG.md to keep track of changes.
* Added tests to the feed test class to cover queries that are below and
beyond the normal page spans.
* Fixed feed to give HTTP 404 errors instead of HTTP 500 errors when
attempting to access a page index that is out of range (above or below).


0.1.0
-----

Initial release.
