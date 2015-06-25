"""Creates the Atom feed for the major PREMIS events."""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.feedgenerator import Atom1Feed
from django.core.paginator import Paginator

from .models import Event


class MajorEventLogFeed(Atom1Feed):
    """Custom Atom Feed for Event objects.

    The only changes between this custom feed and the base Atom Feed
    are that this feed specifies its mime_type as 'application/xml',
    pagination is added, the 'alternate' link is removed.
    """

    mime_type = 'application/xml'

    def add_root_elements(self, handler):
        handler.addQuickElement(u'title', self.feed['title'])
        handler.addQuickElement(
            u'link', '', {u'rel': u'self', u'href': self.feed['feed_url']}
        )
        handler.addQuickElement(u'id', self.feed['id'])
        handler.startElement(u'author', {})
        handler.addQuickElement(u'name', self.feed['author_name'])
        handler.addQuickElement(u'uri', self.feed['author_link'])
        handler.endElement(u'author')
        handler.addQuickElement(u'subtitle', self.feed['subtitle'])
        handler.addQuickElement(
            u'link',
            '',
            {u'rel': u'first', u'href': self.feed['link'] + '?p=1'}
        )
        handler.addQuickElement(
            u'link',
            '',
            {
                u'rel': u'last',
                u'href': self.feed['link'] + '?p=%s' % self.feed['last_link']
            }
        )
        if self.feed.get('prev_link', None) is not None:
            handler.addQuickElement(
                u'link',
                '',
                {
                    u'rel': u'previous',
                    u'href': '%s?p=%s' % (
                        self.feed['link'],
                        self.feed['prev_link']
                    )
                }
            )
        if self.feed.get('next_link', None) is not None:
            handler.addQuickElement(
                u'link',
                '',
                {
                    u'rel': u'next',
                    u'href': '%s?p=%s' % (
                        self.feed['link'],
                        self.feed['next_link']
                    )
                }
            )


class LatestEventsFeed(Feed):
    feed_type = MajorEventLogFeed
    title = 'PREMIS Major Event Log'
    link = reverse_lazy('major-event-log:feed')
    subtitle = '10 most recent major PREMIS events.'
    author_name = 'Major Event Log'
    author_link = 'http://digital2.library.unt.edu/name/nm0005293/'

    def get_object(self, request):
        display = Event.objects.order_by('-date')
        return (display, request.GET.get('p'))

    def feed_extra_kwargs(self, display):
        extra_dict = {}
        d = Paginator(display[0], 10)
        p = display[1]
        if p is None:
            p = 1
        cur_page = d.page(p)
        if cur_page.has_next():
            extra_dict.setdefault('next_link', cur_page.next_page_number())
        if cur_page.has_previous():
            extra_dict.setdefault('prev_link', cur_page.previous_page_number())
        extra_dict.setdefault('last_link', str(d.num_pages))
        return extra_dict

    def items(self, display):
        p = display[1]
        if p is None:
            p = 1
        d = Paginator(display[0], 10)
        return d.page(p).object_list

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.detail

    def item_link(self, item):
        return reverse('major-event-log:event_details', args=[item.pk])

    def item_updateddate(self, item):
        return item.entry_modified
