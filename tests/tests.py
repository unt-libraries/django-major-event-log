import os

from lxml import etree

from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.http import Http404

from major_event_log.models import Event
from major_event_log import views
from major_event_log import feeds


def create_event(title='test', outcome='Success', name='John Doe'):
    """Create an event for testing."""
    if outcome == 'Success':
        outcome = ('http://purl.org/NET/UNTL/vocabularies/eventOutcomes/'
                   '#success')
    else:
        outcome = ('http://purl.org/NET/UNTL/vocabularies/eventOutcomes/'
                   '#failure')
    date = timezone.now()
    event = Event.objects.create(
        title=title,
        detail='none',
        outcome=outcome,
        outcome_detail='none',
        date=date,
        contact_name=name,
        contact_email='admin@email.com')
    return event


class TestURLs(TestCase):
    """Test that each existing URL is acknowledged with an HTTP 200."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.event = create_event()

    def test_index_url(self):
        """Check that the index URL receives an HTTP 200."""
        url = reverse('major-event-log:index')
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_details_url(self):
        """Check that the event_details URL receives an HTTP 200."""
        url = reverse('major-event-log:event_details', args=[self.event.id])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_atom_url(self):
        """Check that the event_atom URL receives an HTTP 200."""
        url = reverse('major-event-log:event_atom', args=[self.event.id])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_premis_url(self):
        """Check that the event_premis URL receives an HTTP 200."""
        url = reverse('major-event-log:event_premis', args=[self.event.id])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_feed_url(self):
        """Check that the feed URL receives an HTTP 200."""
        url = reverse('major-event-log:feed')
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_about_url(self):
        """Check that the about URL receives an HTTP 200."""
        url = reverse('major-event-log:about')
        self.assertEqual(self.client.get(url).status_code, 200)


class TestViewsCalled(TestCase):
    """Test that the correct views are called with each URL."""

    def test_event_details_view_called(self):
        """Check that the event_details URL pattern calls the correct view."""
        uuid = '88888888-4444-4444-a444-121212121212'
        url = reverse('major-event-log:event_details', args=[uuid])
        self.assertEqual(resolve(url).func, views.event_details)

    def test_event_atom_view_called(self):
        """Check that the event_atom URL pattern calls the correct view."""
        uuid = '88888888-4444-4444-a444-121212121212'
        url = reverse('major-event-log:event_atom', args=[uuid])
        self.assertEqual(resolve(url).func, views.event_atom)

    def test_event_premis_view_called(self):
        """Check that the event_premis URL pattern calls the correct view."""
        uuid = '88888888-4444-4444-a444-121212121212'
        url = reverse('major-event-log:event_premis', args=[uuid])
        self.assertEqual(resolve(url).func, views.event_premis)

    def test_about_view_called(self):
        """Check that the about URL pattern calls the correct view."""
        url = reverse('major-event-log:about')
        self.assertEqual(resolve(url).func, views.about)


class TestFeed(TestCase):
    """Test the custom pagination functionality added to the feed."""

    @classmethod
    def setUpTestData(cls):
        [create_event() for _ in range(31)]

    def test_has_first_link(self):
        """Check that the href on the `first` link is present and
        correct.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 2})
        feed = etree.fromstring(response.content)

        link = feed.xpath(
            '/ns:feed/ns:link[@rel=\'first\']',
            namespaces={'ns': 'http://www.w3.org/2005/Atom'}
        )
        self.assertTrue('/feed/?p=1' in link[0].attrib.get('href'))

    def test_has_next_link(self):
        """Check that the href on the `next` link is present and
        correct.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 2})
        feed = etree.fromstring(response.content)

        link = feed.xpath(
            '/ns:feed/ns:link[@rel=\'next\']',
            namespaces={'ns': 'http://www.w3.org/2005/Atom'}
        )
        self.assertTrue('/feed/?p=3' in link[0].attrib.get('href'))

    def test_has_previous_link(self):
        """Check that the href on the `previous` link is present and
        correct.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 2})
        feed = etree.fromstring(response.content)

        link = feed.xpath(
            '/ns:feed/ns:link[@rel=\'previous\']',
            namespaces={'ns': 'http://www.w3.org/2005/Atom'}
        )

        self.assertTrue('/feed/?p=1' in link[0].attrib.get('href'))

    def test_has_last_link(self):
        """Check that the href on the `last` link is present and
        correct.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 2})
        feed = etree.fromstring(response.content)

        link = feed.xpath(
            '/ns:feed/ns:link[@rel=\'last\']',
            namespaces={'ns': 'http://www.w3.org/2005/Atom'}
        )
        self.assertTrue('/feed/?p=4' in link[0].attrib.get('href'))

    def test_number_of_items_per_page(self):
        """Check that, at most, 10 events are listed per page."""
        url = reverse('major-event-log:feed')
        response = self.client.get(url)
        feed = etree.fromstring(response.content)

        entries = feed.xpath(
            '/ns:feed/ns:entry',
            namespaces={'ns': 'http://www.w3.org/2005/Atom'}
        )
        self.assertEqual(len(entries), 10)

    def test_page_below_zero(self):
        """Check that a query for a page < 0 receives an HTTP 404 error."""
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': -4})
        self.assertEqual(response.status_code, 404)

    def test_page_zero(self):
        """Check that a query for page 0 receives an HTTP 404 error."""
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 0})
        self.assertEqual(response.status_code, 404)

    def test_page_beyond_last(self):
        """
        Check that a query for a page beyond the last page receives an
        HTTP 404 error.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 10000})
        self.assertEqual(response.status_code, 404)

    def test_page_not_integer(self):
        """
        Check that a query for a page that is not an integer receives an
        HTTP 404 error.
        """
        url = reverse('major-event-log:feed')
        response = self.client.get(url, {'p': 'five'})
        self.assertEqual(response.status_code, 404)


class TestTemplateUsed(TestCase):
    """Test that the correct template is called by the views."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.event = create_event()

    def test_index_template_used(self):
        """Check that the correct template is used by the index view."""
        url = reverse('major-event-log:index')
        template = 'major-event-log/index.html'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_details_template_used(self):
        """Check that the right template is used by the event_details view."""
        url = reverse('major-event-log:event_details', args=[self.event.id])
        template = 'major-event-log/event_details.html'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_atom_template_used(self):
        """Check that the correct template is used by the event_atom view."""
        url = reverse('major-event-log:event_atom', args=[self.event.id])
        template = 'major-event-log/event_atom.xml'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_premis_template_used(self):
        """Check that the correct template is used by the event_premis view."""
        url = reverse('major-event-log:event_premis', args=[self.event.id])
        template = 'major-event-log/event_premis.xml'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_about_template_used(self):
        """Check that the correct template is used by the about view."""
        url = reverse('major-event-log:about')
        template = 'major-event-log/about.html'
        self.assertTemplateUsed(self.client.get(url), template)


class TestGetEventOr404(TestCase):
    """Tests that the function returns the specified event or an HTTP 404."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.event = create_event()

    def test_get_event_or_404_with_uuid_in_db(self):
        """Check that an event is returned when an existing UUID is given."""
        event = views.get_event_or_404(str(self.event.id))
        self.assertIsInstance(event, Event)

    def test_get_event_or_404_with_uuid_not_in_db(self):
        """Check that the function returns 404 for UUID not in db."""
        uuid = 'd7768443-04e2-45d2-b71f-2b716bf13f13'
        with self.assertRaises(Http404):
            views.get_event_or_404(uuid)

    def test_get_event_or_404_with_invalid_uuid(self):
        """Check that the function returns 404 for invalid UUID."""
        # Test with an id that is too short.
        with self.assertRaises(Http404):
            views.get_event_or_404('abcd-1234')
        # Test with an id that has non hexadecimal values.
        with self.assertRaises(Http404):
            views.get_event_or_404('z7768443-04z2-45q2-y71m-2w716px13uzz')


class TestModelMethods(TestCase):
    """Tests correct functionality of the 2 methods in the Event model."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.event = create_event()
        cls.event_failure = create_event(outcome='Failure')

    def test_get_absolute_url(self):
        """Check that the method returns the expected absolute URL.

        This method should return the URL of the event details page
        for that specific event.
        """
        expected = reverse('major-event-log:event_details',
                           args=[self.event.id])
        self.assertEqual(self.event.get_absolute_url(), expected)

    def test_is_success_with_success(self):
        """Check that True is returned when the outcome was a success."""
        self.assertEqual(self.event.is_success(), True)

    def test_is_success_with_failure(self):
        """Check that False is returned when the outcome was a failure."""
        self.assertEqual(self.event_failure.is_success(), False)


class TestEventsUsed(TestCase):
    """Tests to make sure the correct events are being processed."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.events = []
        for i in range(11):
            cls.events.append(create_event())

    def test_index_events(self):
        """Check that the index page shows the most recent 10 events."""
        response = self.client.get(reverse('major-event-log:index'))
        for event in self.events[1:11]:
            self.assertIn(event, response.context['events'])

    def test_event_details_event(self):
        """Check that the event_details page shows the correct event."""
        response = self.client.get(reverse('major-event-log:event_details',
                                           args=[self.events[0].id]))
        # Check that the correct event is passed in the context.
        self.assertEqual(response.context['event'], self.events[0])

    def test_event_atom_event(self):
        """Check that the event_atom page is using the correct event."""
        response = self.client.get(reverse('major-event-log:event_atom',
                                           args=[self.events[0].id]))
        self.assertEqual(response.context['event'], self.events[0])

    def test_event_premis_event(self):
        """Check that the event_premis page is using the correct event."""
        response = self.client.get(reverse('major-event-log:event_premis',
                                           args=[self.events[0].id]))
        self.assertEqual(response.context['event'], self.events[0])

    def test_feed_events(self):
        """Check that only the latest 10 events are included in the feed."""
        response = self.client.get(reverse('major-event-log:feed'))
        self.assertNotContains(response, self.events[0].id)
        for event in self.events[1:11]:
            self.assertContains(response, event.id)


class TestXML(TestCase):
    """Test the validity of the produced XML."""

    @classmethod
    def setUpTestData(cls):
        """Set up the events for use in the tests in this class."""
        cls.event = create_event()
        cls.factory = RequestFactory()

    def get_schema(self, schema_name):
        """Retrieves the XML schema and returns an XML schema validator."""
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'data')
        schema_path = os.path.join(data_path, schema_name)
        with open(schema_path, 'r') as schema_file:
            schema_root = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_root)
        return schema

    def test_atom_xml(self):
        """Validates the Atom items against their schema."""
        request = self.factory.get('/')
        response = views.event_atom(request, str(self.event.id))
        schema = self.get_schema('atom-premis_schema.xsd')
        atom_item = etree.fromstring(response.content)
        self.assertTrue(schema.validate(atom_item))

    def test_event_premis_xml(self):
        """Validates the PREMIS XML against its schema."""
        request = self.factory.get('/')
        response = views.event_premis(request, str(self.event.id))
        schema = self.get_schema('premis_schema.xsd')
        premis = etree.fromstring(response.content)
        self.assertTrue(schema.validate(premis))

    def test_feed_xml(self):
        """Validates the Atom feed against its schema."""
        atom_feed = feeds.LatestEventsFeed()
        request = self.factory.get('/')
        response = atom_feed(request)
        premis = etree.fromstring(response.content)
        schema = self.get_schema('atom_schema.xsd')
        self.assertTrue(schema.validate(premis))
