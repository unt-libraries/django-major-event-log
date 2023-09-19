Django Major Event Log App
============================================================

[![Build Status](https://github.com/unt-libraries/django-major-event-log/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/django-major-event-log/actions)
[![Docs Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://django-major-event-log.readthedocs.org)
[![PyPI](https://img.shields.io/pypi/v/django-major-event-log.svg)](https://pypi.python.org/pypi/django-major-event-log)

About
--------------------------

This Django application is designed to keep track of digital preservation events using the
[PREMIS](http://www.loc.gov/standards/premis/schemas.html) Event model. The app
takes care of both creating and viewing these events. The admin site is responsible
for managing the actual events, which includes creating them as well as making modifications
to the event date, contact info, description, etc. The other pages are responsible for
displaying events with various levels of detail.


Requirements
--------------------------

- Django 4.2
- Python 3.8-3.10


Installation
--------------------------

1.  Install the app
    ```sh
          $ git clone git@github.com:unt-libraries/django-major-event-log.git

          $ cd django-major-event-log
          
          $ python setup.py install
    ```

2.  Add app and all dependencies to INSTALLED_APPS.
    ```python
          INSTALLED_APPS = (
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'major_event_log',
          )
    ```

3.  Include the URLs
    ```python
          urlpatterns = [
            path('admin/', admin.site.urls),
            path('major-event-log/', include(('major_event_log.urls', 'major-event-log'),
                namespace="major-event-log"))
          ]
    ```

4.  Migrate/sync the database
    ```sh
          $ python manage.py migrate
    ```


License
-------------------------

See LICENSE


Contributors
-------------------------

django-major-event-log was developed at the UNT Libraries.

Contributors:

* [Gio Gottardi](https://github.com/somexpert)
* [Damon Kelley](https://github.com/damonkelley)
* [Madhulika Bayyavarapu](https://github.com/madhulika95b)
* [Gracie Flores-Hays](https://github.com/gracieflores)


Developing/Testing
------------------

Read the latest documentation [here](http://django-major-event-log.readthedocs.org/en/latest/developing.html).
