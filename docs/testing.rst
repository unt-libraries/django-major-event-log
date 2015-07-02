Testing
=======

Requirements
------------

-  Django == 1.8
-  tox == 2.0
-  lxml == 3.4
-  Python == 2.7
-  Python == 3.4

**System** Requirements
^^^^^^^^^^^^^^^^^^^^^^^

-  libxml2 >= 2.7.0
-  libxslt >= 1.1.23


Running the tests
-----------------

To run the tests in the development environment:

::

    $ python manage.py test ./tests

You can also run the tests with Tox:

::

    $ [sudo] pip install tox
    $ tox
