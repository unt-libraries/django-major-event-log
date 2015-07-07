Developing
==========

Install the requirements

.. code-block:: sh

    $ pip install -r requirements-dev.txt

.. note:: lxml, used in the tests, requires that libxslt and libxml2 be installed on the system.

Clone the git repository:

.. code-block:: sh

    $ git clone https://github.com/unt-libraries/django-major-event-log
    $ cd django-major-event-log

Initialize the database

.. code-block:: sh

    $ python manage.py migrate

Create a superuser so you can create test events

.. code-block:: sh

    $ python manage.py createsuperuser

Start the development server

.. code-block:: sh

    $ python manage.py runserver

You should now be able to access the admin portion of the app at
127.0.0.1:8000/admin/ and the public-facing side of the app at
127.0.0.1:8000/major-event-log/.

Testing
-------

To run the tests in the development environment:

.. code-block:: sh

    $ python manage.py test ./tests

You can also run the tests with Tox:

.. code-block:: sh

    $ [sudo] pip install tox
    $ tox
