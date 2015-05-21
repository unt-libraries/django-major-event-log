"""Define the urls that are part of the app as regex patterns.

Each regex pattern will map to a page of the application and
load the corresponding view.
"""
from django.conf.urls import url

from . import views
from . import feeds

urlpatterns = [
    # Matches root index of app ('/').
    url(r'^$', views.index, name='index'),
    # Matches urls like 'event/123a-4b56c-78d/'.
    url(r'^event/(?P<event_id>[0-9a-z-]+)/$', views.event_detail,
        name='event_detail'),
    # Matches urls like 'event/123a-4b56c-78d.xml/'.
    url(r'^event/(?P<event_id>[0-9a-z-]+)\.xml/$', views.event_atom,
        name='event_atom'),
    # Matches urls like 'event/123a-4b56c-78d.premis.xml/'.
    url(r'^event/(?P<event_id>[0-9a-z-]+)\.premis\.xml/$', views.event_premis,
        name='event_premis'),
    # Matches 'feed/'.
    url(r'^feed/$', feeds.LatestEventsFeed(), name='feed'),
    # Matches 'about/'.
    url(r'^about/$', views.about, name='about'),
]
