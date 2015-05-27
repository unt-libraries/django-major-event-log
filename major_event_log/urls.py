"""Define the urls that are part of the app as regex patterns.

Each regex pattern will map to a page of the application and
load the corresponding view.
"""
from django.conf.urls import url

from . import views
from . import feeds

uuid4 = (r'[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}'
         '-?[a-f0-9]{12}')
urlpatterns = [
    # Matches root index of app ('/').
    url(r'^$', views.index, name='index'),
    # Matches urls like 'event/123a-4b56c-78d/'.
    url(r'^event/(?P<event_id>' + uuid4 + r')/$', views.event_details,
        name='event_details'),
    # Matches urls like 'event/123a-4b56c-78d.xml/'.
    url(r'^event/(?P<event_id>' + uuid4 + r')\.xml/$', views.event_atom,
        name='event_atom'),
    # Matches urls like 'event/123a-4b56c-78d.premis.xml/'.
    url(r'^event/(?P<event_id>' + uuid4 + r')\.premis\.xml/$',
        views.event_premis, name='event_premis'),
    # Matches 'feed/'.
    url(r'^feed/$', feeds.LatestEventsFeed(), name='feed'),
    # Matches 'about/'.
    url(r'^about/$', views.about, name='about'),
]
