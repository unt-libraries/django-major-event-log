"""Defines all the views, which load the requested pages.

These views will render the appropriate web pages based on
templates defined in the 'templates/major-event-log' directory.
"""
import uuid

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404

from .models import Event


def is_uuid(event_id):
    """Checks that the event_id is a valid uuid instance."""
    try:
        uuid.UUID(event_id)
    except ValueError:
        return False
    return True


def index(request):
    """Loads the index, or 'home page' of the major event log app."""
    events = Event.objects.order_by('-date')
    context = {'events': events}
    return render(request, 'major-event-log/index.html', context)


def event_details(request, event_id):
    """Loads the event details page of the event with the given id."""
    if is_uuid(event_id) is True:
        event = get_object_or_404(Event.objects, id=event_id)
    else:
        raise Http404("Invalid event id")
    context = {'event': event}
    return render(request, 'major-event-log/event_details.html', context)


def event_atom(request, event_id):
    """Loads the ATOM record for the event with the given id."""
    if is_uuid(event_id) is True:
        event = get_object_or_404(Event.objects, id=event_id)
    else:
        raise Http404("Invalid event id")
    event_detail_url = request.build_absolute_uri(
        reverse('major-event-log:event_details', args=[event_id]))
    context = {'event': event, 'full_url': event_detail_url}
    return render(request, 'major-event-log/event_atom.xml', context,
                  content_type='text/xml; charset=utf-8')


def event_premis(request, event_id):
    """Loads the PREMIS event item for the event with the given id."""
    if is_uuid(event_id) is True:
        event = get_object_or_404(Event.objects, id=event_id)
    else:
        raise Http404("Invalid event id")
    context = {'event': event}
    return render(request, 'major-event-log/event_premis.xml', context,
                  content_type='text/xml; charset=utf-8')


def about(request):
    """Loads the 'about' page."""
    return render(request, 'major-event-log/about.html')
