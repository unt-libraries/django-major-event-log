Developing
==========

Install the requirements

::

    $ pip install -r requirements.txt

(note that lxml, used in the tests, requires that libxslt and libxml2 be
installed on the system)

Clone the git repository:

::

    $ git clone https://github.com/unt-libraries/django-major-event-log
    $ cd django-major-event-log

Initialize the database

::

    $ python manage.py migrate

Create a superuser so you can create test events

::

    $ python manage.py createsuperuser

Start the development server

::

    $ python manage.py runserver

(press Ctrl-c to stop the development server)

You should now be able to access both the admin portion of the app at
127.0.0.1:8000/admin/, or the public-facing side of the app at
127.0.0.1:8000/major-event-log/.

Testing
-------

To run the tests in the development environment:

::

    $ python manage.py test ./tests

You can also run the tests with Tox:

::

    $ [sudo] pip install tox
    $ tox
