Notice!
------------------------------------------------------------

**This application is still being developed! Major components are still in an
unfinished state!**

Django Major Event Log App [![Build Status](https://travis-ci.org/unt-libraries/django-major-event-log.svg?branch=master)](https://travis-ci.org/unt-libraries/django-major-event-log)
============================================================

About
--------------------------

This Django appplication is designed to keep track of major PREMIS events.
The app takes care of both creating and viewing these events. The admin site is
responsible for managing the actual events, which includes creating them as well
as making modifications to the event date, contact info, description, etc. The
other pages are responsible for displaying events with various levels of
detail.


Requirements
--------------------------

- Django == 1.8
- Python >= 2.7


Installation
--------------------------

1. Install the app

        $ pip install major-event-log

2. Add app and all dependencies to INSTALLED_APPS.

        INSTALLED_APPS = (
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
          'major_event_log',
        )

3. Include the URLs

        urlpatterns = [
          url(r'^admin/', include(admin.site.urls)),
          url(r'^major-event-log/', include('major_event_log.urls',
            namespace="major-event-log"))
        ]

4. Migrate/sync the database

        $ python manage.py migrate major-event-log

5. Configure static files

        STATIC_URL = '/static/'


License
-------------------------

See LICENSE


Contributors
-------------------------

django-major-event-log was developed at the UNT Libraries.

Contributors:

* [Gio Gottardi](https://github.com/somexpert)
* [Damon Kelley](https://github.com/damonkelley)


Developing/Testing
------------------

[Read the Docs](http://django-major-event-log.readthedocs.org/en/latest/developing.html)
