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

1. Install with the following command (in the root of the app directory)

        $ pip install major-event-log

2. Add `major_event_log` to your `INSTALLED_APPS`. Be sure to add `django.contrib.admin` (and its dependencies) and `django.contrib.humanize` if they are not already present. Your `INSTALLED_APPS` should look like the following (at the minimum):

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


Developing
-------------------------

#### Requirements ####

- Django == 1.8
- Python >= 2.7

#### Setting up the development environment ####

First, get the source files for the app by cloning the git repository:

    $ git clone https://github.com/unt-libraries/django-major-event-log

and navigate to within the new directory:

    $ cd django-major-event-log

Now, in order to be able to use the app, you must first initialize the database
by running:

    $ python manage.py migrate

You should take this time to create a superuser for the app so you can create
test events that will let you see what the site will look like with a populated
database:

    $ python manage.py createsuperuser

which will guide you through creating a superuser with login credentials that
you can use on the admin portion of the app. Now you should have a development
environment where you can see all the source code and check out the app using
Django's development server. To do so, simply execute the following from the
current location (the root of the git repository):

    $ python manage.py runserver

(press Ctrl-c to stop the development server)

You should now be able to access both the admin portion of the app at
127.0.0.1:8000/admin/, or the public-facing side of the app at
127.0.0.1:8000/major-event-log/.


Testing
-------

#### Requirements ####

- Django == 1.8
- tox == 2.0
- lxml == 3.4
- Python == 2.7
- Python == 3.4

#### **System** Requirements ####

- libxml2 >= 2.7.0
- libxslt >= 1.1.23

#### Running the tests ####

To run the tests in the development environment:

    $ python manage.py test ./tests

You can also run the tests with Tox:

    $ [sudo] pip install tox
    $ tox
