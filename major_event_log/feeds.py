from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

from .models import Event

class LatestEventsFeed(Feed):
    feed_type = Atom1Feed
    title = "PREMIS major event log"
    link = "/major-event-log"
    description = "Latest updates to PREMIS major events."    

    def items(self):
        return Event.objects.order_by('-date')[:10]

    def item_title(self, item):
        return item.title

    def item_subtitle(self, item):
        return item.detail

    def item_link(self, item):
        return reverse('major-event-log:event_detail', args=[item.pk])
