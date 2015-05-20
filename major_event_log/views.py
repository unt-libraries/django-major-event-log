from django.shortcuts import render
from django.http import HttpResponse

from .models import Event

def index(request):
    events = Event.objects.order_by('-date')
    context = {'events': events}
    return render(request, 'major_event_log/index.html', context)

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'major_event_log/event_detail.html', context)

def event_atom(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {'event': event, 'full_url': request.build_absolute_uri()[:-5] + '/'}
    return render(request, 'major_event_log/event_atom.xml', context, content_type='text/xml; charset=utf-8')

def event_premis(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {'event': event}
    return render(request, 'major_event_log/event_premis.xml', context, content_type='text/xml; charset=utf-8')

def about(request):
    return render(request, 'major_event_log/about.html')
