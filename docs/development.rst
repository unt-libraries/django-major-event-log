Developing
==========

Requirements
------------

-  Django == 1.8
-  Python >= 2.7


Setting up the development environment
--------------------------------------

First, get the source files for the app by cloning the git repository:

::

    $ git clone https://github.com/unt-libraries/django-major-event-log

and navigate to within the new directory:

::

    $ cd django-major-event-log

Now, in order to be able to use the app, you must first initialize the
database by running:

::

    $ python manage.py migrate

You should take this time to create a superuser for the app so you can
create test events that will let you see what the site will look like
with a populated database:

::

    $ python manage.py createsuperuser

which will guide you through creating a superuser with login credentials
that you can use on the admin portion of the app. Now you should have a
development environment where you can see all the source code and check
out the app using Django's development server. To do so, simply execute
the following from the current location (the root of the git
repository):

::

    $ python manage.py runserver

(press Ctrl-c to stop the development server)

You should now be able to access both the admin portion of the app at
127.0.0.1:8000/admin/, or the public-facing side of the app at
127.0.0.1:8000/major-event-log/.
