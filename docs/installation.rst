Installation
============

Requirements
------------

-  Django == 1.8
-  Python >= 2.7

Installing
----------

1. Install the app

   ::

       $ pip install major-event-log

2. Add app and all dependencies to INSTALLED\_APPS.

   ::

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

   ::

       urlpatterns = [
         url(r'^admin/', include(admin.site.urls)),
         url(r'^major-event-log/', include('major_event_log.urls',
           namespace="major-event-log"))
       ]

4. Migrate/sync the database

   ::

       $ python manage.py migrate major-event-log
