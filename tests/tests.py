import xml.etree.ElementTree as ET

from django.core.urlresolvers import reverse, resolve
from django.utils import timezone
from django.test import TestCase
from django.http import Http404

from major_event_log.models import Event
from major_event_log import views


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

    def test_index_url(self):
        """Check that the index URL receives an HTTP 200."""
        url = reverse('major-event-log:index')
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_details_url(self):
        """Check that the event_details URL receives an HTTP 200."""
        uuid = create_event().id
        url = reverse('major-event-log:event_details', args=[uuid])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_atom_url(self):
        """Check that the event_atom URL receives an HTTP 200."""
        uuid = create_event().id
        url = reverse('major-event-log:event_atom', args=[uuid])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_event_premis_url(self):
        """Check that the event_premis URL receives an HTTP 200."""
        uuid = create_event().id
        url = reverse('major-event-log:event_premis', args=[uuid])
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


class TestTemplateUsed(TestCase):
    """Test that the correct template is called by the views."""

    def test_index_template_used(self):
        """Check that the correct template is used by the index view."""
        url = reverse('major-event-log:index')
        template = 'major-event-log/index.html'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_details_template_used(self):
        """Check that the right template is used by the event_details view."""
        uuid = create_event().id
        url = reverse('major-event-log:event_details', args=[uuid])
        template = 'major-event-log/event_details.html'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_atom_template_used(self):
        """Check that the correct template is used by the event_atom view."""
        uuid = create_event().id
        url = reverse('major-event-log:event_atom', args=[uuid])
        template = 'major-event-log/event_atom.xml'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_event_premis_template_used(self):
        """Check that the correct template is used by the event_premis view."""
        uuid = create_event().id
        url = reverse('major-event-log:event_premis', args=[uuid])
        template = 'major-event-log/event_premis.xml'
        self.assertTemplateUsed(self.client.get(url), template)

    def test_about_template_used(self):
        """Check that the correct template is used by the about view."""
        url = reverse('major-event-log:about')
        template = 'major-event-log/about.html'
        self.assertTemplateUsed(self.client.get(url), template)


class TestGetEventOr404(TestCase):
    """Tests that the function returns the specified event or an HTTP 404."""

    def test_get_event_or_404_with_uuid_in_db(self):
        """Check that an event is returned when an existing UUID is given."""
        uuid = str(create_event().id)
        event = views.get_event_or_404(uuid)
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

    def test_get_absolute_url(self):
        """Check that the method returns the expected absolute URL.

        This method should return the URL of the event details page
        for that specific event.
        """
        event = create_event()
        expected = reverse("major-event-log:event_details", args=[event.id])
        self.assertEqual(event.get_absolute_url(), expected)

    def test_is_success_with_success(self):
        """Check that True is returned when the outcome was a success."""
        event = create_event()
        self.assertEqual(event.is_success(), True)

    def test_is_success_with_failure(self):
        """Check that False is returned when the outcome was a failure."""
        event = create_event(outcome='Failure')
        self.assertEqual(event.is_success(), False)


class TestEventsUsed(TestCase):
    """Tests to make sure the correct events are being processed."""

    def test_index_events(self):
        """Check that the index page shows the most recent 10 events."""
        events = []
        for i in range(4):
            events.append(create_event())
        response = self.client.get(reverse('major-event-log:index'))
        for event in events:
            self.assertIn(event, response.context['events'])

    def test_event_details_event(self):
        """Check that the event_details page shows the correct event."""
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_details',
                                           args=[event.id]))
        # Check that the correct event is passed in the context.
        self.assertEqual(response.context['event'], event)

    def test_event_atom_event(self):
        """Check that the event_atom page is using the correct event."""
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_atom',
                                           args=[event.id]))
        self.assertEqual(response.context['event'], event)

    def test_event_premis_event(self):
        """Check that the event_premis page is using the correct event."""
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_premis',
                                           args=[event.id]))
        self.assertEqual(response.context['event'], event)

    def test_feed_events(self):
        """Check that only the latest 10 events are included in the feed."""
        events = []
        for i in range(11):
            events.append(create_event())
        response = self.client.get(reverse('major-event-log:feed'))
        self.assertNotContains(response, events[0].id)
        for event in events[1:]:
            self.assertContains(response, event.id)


class TestXML(TestCase):
    """Test the validity of the produced XML."""

    def test_event_atom_xml(self):
        """Checks for the correct structure within the Atom XML."""
        namespace = {'default': 'http://www.w3.org/2005/Atom'}
        expected_xml_structure = [
            './default:title',
            './default:id',
            './default:updated',
            './default:author/default:name',
            './default:content'
        ]
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_atom',
                                           args=[event.id]))
        atom = ET.fromstring(response.content)
        for xpath in expected_xml_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))

    def test_event_premis_xml(self):
        """Checks for the correct structure within the Atom XML."""
        namespace = {'prms': 'info:lc/xmlns/premis-v2'}
        expected_premis_structure = [
            './prms:eventDetail',
            './prms:eventOutcomeInformation/prms:eventOutcomeDetail',
            './prms:eventOutcomeInformation/prms:eventOutcome',
            './prms:eventType',
            './prms:linkingAgentIdentifier/prms:linkingAgentIdentifierValue',
            './prms:linkingAgentIdentifier/prms:linkingAgentIdentifierType',
            './prms:eventIdentifier/prms:eventIdentifierValue',
            './prms:eventIdentifier/prms:eventIdentifierType',
            './prms:eventDateTime'
        ]
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_premis',
                                           args=[event.id]))
        # Make sure that the PREMIS event has the expected structure.
        atom = ET.fromstring(response.content)
        for xpath in expected_premis_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))

    def test_feed_xml(self):
        """Checks for the correct structure within the Atom feed's XML."""
        namespace = {'default': 'http://www.w3.org/2005/Atom'}
        expected_feed_structure = [
            './default:title',
            './default:link',
            './default:id',
            './default:updated',
            './default:subtitle',
            './default:entry'
        ]
        create_event()
        response = self.client.get(reverse('major-event-log:feed'))
        atom = ET.fromstring(response.content)
        for xpath in expected_feed_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))
