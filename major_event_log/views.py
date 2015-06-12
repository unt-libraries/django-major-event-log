"""Defines all the views, which load the requested pages.

These views will render the appropriate web pages based on
templates defined in the 'templates/major-event-log' directory.
"""
import uuid

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Event


def get_event_or_404(event_id):
    """Retrieves event, if possible. If not, raises http 404 response.

    Checks two separate things related to the given event_id. The first
    is that the event_id is a well-formed uuid. If the event_id is a
    valid uuid, then the get_object_or_404 function is called to check
    that the valid uuid actually refers to an event that has already
    been created in the db. If either of these checks fail, then an
    http 404 response is sent.
    """
    try:
        uuid.UUID(event_id)
    except ValueError:
        raise Http404("Invalid event id")
    return get_object_or_404(Event.objects, id=event_id)


def index(request):
    """Loads the index, or 'home page' of the major event log app."""
    events = Event.objects.order_by('-date')
    context = {'events': events}
    return render(request, 'major-event-log/index.html', context)


def event_details(request, event_id):
    """Loads the event details page of the event with the given id."""
    event = get_event_or_404(event_id)
    context = {'event': event}
    return render(request, 'major-event-log/event_details.html', context)


def event_atom(request, event_id):
    """Loads the Atom record for the event with the given id."""
    event = get_event_or_404(event_id)
    event_detail_url = request.build_absolute_uri(event.get_absolute_url())
    context = {'event': event, 'event_details_url': event_detail_url}
    return render(request, 'major-event-log/event_atom.xml', context,
                  content_type='text/xml; charset=utf-8')


def event_premis(request, event_id):
    """Loads the PREMIS event item for the event with the given id."""
    event = get_event_or_404(event_id)
    context = {'event': event}
    return render(request, 'major-event-log/event_premis.xml', context,
                  content_type='text/xml; charset=utf-8')


def about(request):
    """Loads the 'about' page."""
    return render(request, 'major-event-log/about.html')
