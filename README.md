Notice!
------------------------------------------------------------

**This application is still being developed! Major components are still in an
unfinished state!**

Django Major Event Log App [![Build Status](https://travis-ci.org/unt-libraries/django-major-event-log.svg?branch=master)](https://travis-ci.org/unt-libraries/django-major-event-log)
============================================================

About
--------------------------

This django appplication is designed to keep track of major premis events.
The app takes care of both creating and viewing these events. The admin site is
reponsible for managing the actual events, which includes creating them as well
as making modifications to the event date, contact info, description, etc. The
other pages are responsible for displaying events with various levels of
detail.

Each premis event MUST contain the following information:

* Event ID
* Title
* Details
* Outcome
* Outcome Details
* Event Date
* Event Creation Date
* Event Last Modified Date
* Contact Name
* Contact Email

The **Index** page displays all of the created events, in reverse chronological
order (most recent Event Date first). The title, event date, ID, and
outcome are all displayed on this page. The title of each event is
clickable and takes you to the details page for that specific event.

The **Event Details** page displays all the information about a specific event.
On top of displaying all the information in a human-readable form, this page
provides links to the premis xml representation of the event, as well as an
atom item for the event, which contains all the premis xml wrapped in the atom
item.

The **Atom Feed** page, linked to in the navigation bar of each html page,
provides an atom feed for the ten most recent events. Again, these are
sorted by the event date, not the creation or modified dates.

Finally, there is also a small `About` page which contains a description of the
application.

Requirements
--------------------------

### Deployment ###

Django == 1.8 `sudo pip install django`
Python >= 2.7

### Development ###

See Deployment

#### Testing ####

All requirements from Development
lxml
flake8
Python 2.7
Python 3.4

Installation
--------------------------

1.  Download Source

    To get the application, download the source code from the Github repository
    [here](https://github.com/unt-libraries/django-major-event-log).

2.  Install

    Install with `pip install https://github.com/unt-libraries/django-major-event-log`

3.  Hook into Django.
    asldfjalsdfjasd
License
-------------------------

See LICENSE

Contributors
-------------------------

Django-major-event-log was developed at the UNT Libraries.

Contributors:

* [Gio Gottardi](https://github.com/somexpert)
* [Damon Kelley](https://github.com/damonkelley)

Developing/Testing
-------------------------

I suggest doing the following within a virtual environment. To do so, you will
first need to install virtualenv with the following command:
`$ [sudo] pip install virtualenv`
Then, you will need to set up a virtual environment by navigating to the
location you want your environment created and running:
`$ virtualenv --python=python2.7 new_virtualenv_name`
This will create a directory called new\_virtualenv\_name that is the virutal
environment. Next, you'll need to get inside the new directory with:
`$ cd new\_virtualenv\_name`
and then activate the new virtual environment:
`$ source ./bin/activate` (after testing, exit the virtual environment with `$ deactivate`)
You will need to install Django into the virtual env to be able to test out the
app with Django's development server:
`$ pip install django==1.8`
Now you need to get the source files for the app by cloning the git repository:
`$ git clone https://github.com/unt-libraries/django-major-event-log`
and navigate to within the new directory:
`$ cd django-major-event-log`
Now, in order to be able to use the app, you must first initialize the database
by running:
`$ python manage.py migrate`
You should take this time to create a superuser for the app so you can create
test events that will let you see what the site will look like with a populated
database:
`$ python manage.py createsuperuser`
which will guide you through creating a super-user with login credentials that
you can use on the admin portion of the app. Now you should have a development 
environment where you can see all the source code and check out the app using
Django's development server. To do so, simply execute the following from the
current location (the root of the git repository):
`$ python manage.py runserver` (press Ctrl-c to stop the development server)
You should now be able to access both the admin portion of the app at
127.0.0.1:8000/admin/, or the public-facing side of the app at
127.0.0.1:8000/major-event-log/.

#### Running the tests ####

Simply invoke the tox test runner by running `tox` anywhere within the app (if
you are running in a virtual environment, you will first need to install tox
with `$ pip install tox`).
`$ tox`
If you don't wish to test using tox, you can also simply use Django's test
runner by navigating to the root of the git repositor and running:
`$ python manage.py test ./tests`
Note that the python test runner will only run the tests against the current
version of Python, and will also not run a flake8 test. Conversely, tox will
run the test suite against multiple versions of Python (2.7 and 3.4) as well as multiple
versions of Django (1.8 and the master branch of Django), and will also run a
flake8 check on the source code.
