Installation
------------

1. Install with the following command (in the root of the app directory)

   ::

       $ [sudo] pip install major-event-log

2. Add ``major_event_log`` to your ``INSTALLED_APPS``. Be sure to add
   ``django.contrib.admin`` (and its dependencies) and
   ``django.contrib.humanize`` if they are not already present. Your
   ``INSTALLED_APPS`` should look like the following (at the minimum):

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

       $ python manage.py migrate majore-event-log

5. Configure static files

   ::

       STATIC_URL = '/static/'
