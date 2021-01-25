"""Define the URLs that are part of the app as regex patterns.

Each regex pattern will map to a page of the application and
load the corresponding view.
"""
from django.urls import path

from . import views
from . import feeds


urlpatterns = [
    # Matches root index of app ('/').
    path('', views.EventList.as_view(), name='index'),
    # Matches urls like 'event/123a-4b56c-78d.premis.xml'.
    path('event/<slug:event_id>.premis.xml',
         views.event_premis, name='event_premis'),
    # Matches URLs like 'event/123a-4b56c-78d.xml'.
    path('event/<slug:event_id>.xml', views.event_atom,
         name='event_atom'),
    # Matches URLs like 'event/123a-4b56c-78d/'.
    path('event/<slug:event_id>/', views.event_details,
         name='event_details'),
    # Matches 'feed/'.
    path('feed/', feeds.LatestEventsFeed(), name='feed'),
    # Matches 'about/'.
    path('about/', views.about, name='about'),
]
