"""Creates the ATOM feed for the major premis events events."""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import Event


class MajorEventLogFeed(Atom1Feed):
    """Custom Atom Feed for Event objects.

    The only change between this custom feed and the base Atom1Feed
    is that this feed specifies its mime_type as 'application/xml'.
    """
    mime_type = 'application/xml'


class LatestEventsFeed(Feed):
    # Custom Atom feed.
    feed_type = MajorEventLogFeed
    # Required tags by the ATOM feed.
    title = "PREMIS Major Event Log"
    link = "/major-event-log/"
    subtitle = "10 most recent major PREMIS events."

    # Show simple, human-readable fields in the event feed.
    def items(self):
        return Event.objects.order_by('-date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.detail

    def item_link(self, item):
        return reverse('major-event-log:event_details', args=[item.pk])
