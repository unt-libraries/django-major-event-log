Installation
============

Requirements
------------

-  Django 1.8 - 1.11
-  Python 2.7, 3.4 - 3.6

Installing
----------

1. Install the app

   .. code-block:: sh

       $ pip install major-event-log

2. Add app and all dependencies to INSTALLED\_APPS.

   .. code-block:: python

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

   .. code-block:: python

       urlpatterns = [
         url(r'^admin/', include(admin.site.urls)),
         url(r'^major-event-log/', include('major_event_log.urls',
           namespace='major-event-log'))
       ]

4. Migrate/sync the database

   .. code-block:: sh

       $ python manage.py migrate
