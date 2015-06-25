"""Creates the Atom feed for the major PREMIS events."""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.feedgenerator import Atom1Feed
from django.core.paginator import Paginator

from .models import Event


class PaginatedFeedTypeMixin(object):

    def _create_link_attr(self, rel, page):
        href = u'{0}?{1}={2}'.format(
            self.feed['link'], self.feed['page_query'], page)

        return {u'rel': rel, u'href': href}

    def add_root_elements(self, handler):
        from django.utils.feedgenerator import rfc3339_date
        handler.addQuickElement("title", self.feed['title'])
        handler.addQuickElement(
            "link", "", {"rel": "alternate", "href": self.feed['link']})

        if self.feed['feed_url'] is not None:
            handler.addQuickElement("link", "", {"rel": "self", "href": self.feed['feed_url']})

        handler.addQuickElement(u'link', '', self._create_link_attr(u'first', 1))
        handler.addQuickElement(u'link', '', self._create_link_attr(u'last', self.feed['last_page']))

        if self.feed.get('prev_page', None) is not None:
            handler.addQuickElement(u'link', '', self._create_link_attr(u'prev_page', self.feed['prev_page']))
        if self.feed.get('next_page', None) is not None:
            handler.addQuickElement(u'link', '', self._create_link_attr(u'next_page', self.feed['next_page']))

        handler.addQuickElement("id", self.feed['id'])
        handler.addQuickElement("updated", rfc3339_date(self.latest_post_date()))

        if self.feed['author_name'] is not None:
            handler.startElement("author", {})
            handler.addQuickElement("name", self.feed['author_name'])
            if self.feed['author_email'] is not None:
                handler.addQuickElement("email", self.feed['author_email'])
            if self.feed['author_link'] is not None:
                handler.addQuickElement("uri", self.feed['author_link'])
            handler.endElement("author")

        if self.feed['subtitle'] is not None:
            handler.addQuickElement("subtitle", self.feed['subtitle'])

        for cat in self.feed['categories']:
            handler.addQuickElement("category", "", {"term": cat})

        if self.feed['feed_copyright'] is not None:
            handler.addQuickElement("rights", self.feed['feed_copyright'])


class MajorEventLogFeed(PaginatedFeedTypeMixin, Atom1Feed):
    """Custom Atom Feed for Event objects.

    The only changes between this custom feed and the base Atom Feed
    are that this feed specifies its mime_type as 'application/xml',
    pagination is added, the 'alternate' link is removed.
    """

    mime_type = 'application/xml'


class PaginatedFeedMixin(object):
    paginator = None
    page = 1
    items_per_page = 2
    page_query = 'page'

    def setup_paginator(self, request, items):
        self.page = request.GET.get(self.page_query, 1)
        self.paginator = Paginator(items, self.items_per_page)

    def get_page(self):
        return self.paginator.page(self.page)

    def get_page_kwargs(self):
        page = self.get_page()

        kwargs = {}

        kwargs.setdefault('page_query', self.page_query)
        if page.has_next():
            kwargs.setdefault('next_page', page.next_page_number())

        if page.has_previous():
            kwargs.setdefault('prev_page', page.previous_page_number())

        kwargs.setdefault('last_page', str(self.paginator.num_pages))
        return kwargs


class LatestEventsFeed(PaginatedFeedMixin, Feed):
    feed_type = MajorEventLogFeed
    title = 'PREMIS Major Event Log'
    link = reverse_lazy('major-event-log:feed')
    subtitle = '10 most recent major PREMIS events.'
    author_name = 'Major Event Log'
    author_link = 'http://digital2.library.unt.edu/name/nm0005293/'
    page_query = 'p'

    def get_object(self, request):
        display = Event.objects.order_by('-date')
        self.setup_paginator(request, display)
        return display

    def feed_extra_kwargs(self, display):
        return self.get_page_kwargs()

    def items(self, obj):
        return self.get_page().object_list

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.detail

    def item_link(self, item):
        return reverse('major-event-log:event_details', args=[item.pk])

    def item_updateddate(self, item):
        return item.entry_modified
