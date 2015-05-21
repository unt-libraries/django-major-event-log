"""Defines all the views, which load the requested pages.

These views will call the render the appropriate web pages based on
templates defined in the 'templates/major-event-log' directory.
"""
from django.shortcuts import render

from .models import Event


def index(request):
    """Loads the index, or 'home page' of the major event log app."""
    events = Event.objects.order_by('-date')
    context = {'events': events}
    return render(request, 'major-event-log/index.html', context)


def event_detail(request, event_id):
    """Loads the event details page of the event with the given id."""
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'major-event-log/event_detail.html', context)


def event_atom(request, event_id):
    """Loads the ATOM record for the event with the given id."""
    event = Event.objects.get(id=event_id)
    context = {'event': event,
               'full_url': request.build_absolute_uri()[:-5] + '/'}
    return render(request, 'major-event-log/event_atom.xml', context,
                  content_type='text/xml; charset=utf-8')


def event_premis(request, event_id):
    """Loads the PREMIS event item for the event with the given id."""
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'major-event-log/event_premis.xml', context,
                  content_type='text/xml; charset=utf-8')


def about(request):
    """Loads the 'about' page."""
    return render(request, 'major-event-log/about.html')
