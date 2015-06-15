import xml.etree.ElementTree as ET

from django.core.urlresolvers import reverse, resolve
from django.utils import timezone
from django.test import TestCase

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


class TestURLsToViews(TestCase):
    """Tests to make sure that URLS get directed to the right views.

    Verifies that the correct information is captured from the urls,
    that the urls get directed correctly (or that the correct error
    is displayed), and that the correct templates get used.
    """

    def test_valid_urls(self):
        """Check that valid URLs get directed to the correct views."""
        uuid = create_event().id
        urls = (reverse('major-event-log:index'),
                reverse('major-event-log:event_details', args=[uuid]),
                reverse('major-event-log:event_atom', args=[uuid]),
                reverse('major-event-log:event_premis', args=[uuid]),
                reverse('major-event-log:feed'),
                reverse('major-event-log:about'))
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_invalid_urls(self):
        """Check that invalid URL requests get an HTTP 404."""
        urls = ('/nothing/',
                '/major-event-log/nothing/',
                '/major-event-log/event/',
                '/major-event-log/feed/nothing/',
                '/major-event-log/about/nothing/')
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 404)

    def test_uuid_match(self):
        """Check that uuid not in db receives an HTTP 404."""
        uuid = '88888888-4444-4444-a444-121212121212'
        response = self.client.get(reverse('major-event-log:event_details',
                                           args=[uuid]))
        self.assertEqual(response.status_code, 404)

    def test_url_uuid_catch(self):
        """Check that the uuid gets caught correctly by the regex."""
        uuid = '88888888-4444-4444-a444-121212121212'
        url = reverse('major-event-log:event_details', args=[uuid])
        self.assertIn(uuid, url)

    def test_correct_view_called(self):
        """Check that urls are resolved to the correct views."""
        uuid = '88888888-4444-4444-a444-121212121212'
        urls = ((reverse('major-event-log:event_details', args=[uuid]),
                    views.event_details),
                (reverse('major-event-log:event_atom', args=[uuid]),
                    views.event_atom),
                (reverse('major-event-log:event_premis', args=[uuid]),
                    views.event_premis),
                (reverse('major-event-log:about'),
                    views.about))
        for url, expected in urls:
            self.assertEqual(resolve(url).func, expected)

    def test_correct_templates_used(self):
        """Check that the right templates are used by the views."""
        uuid = create_event().id
        urls = ((reverse('major-event-log:index'),
                 'major-event-log/index.html'),
                (reverse('major-event-log:event_details', args=[uuid]),
                    'major-event-log/event_details.html'),
                (reverse('major-event-log:event_atom', args=[uuid]),
                    'major-event-log/event_atom.xml'),
                (reverse('major-event-log:event_premis', args=[uuid]),
                    'major-event-log/event_premis.xml'),
                (reverse('major-event-log:about'),
                    'major-event-log/about.html'))
        for url, template in urls:
            self.assertTemplateUsed(self.client.get(url), template)


class TestContentProduced(TestCase):
    """Tests to make sure content is being produced correctly."""

    def test_index_content(self):
        """Check the content of the index page.

        Contents are verified by checking that all existing events
        have been placed in the context.
        """
        events = []
        for i in range(4):
            events.append(create_event())
        response = self.client.get(reverse('major-event-log:index'))
        for event in events:
            self.assertIn(event, response.context['events'])

    def test_event_details_content(self):
        """Check the content of the event_details page.

        Contents are verified by checking that the proper event has
        been placed in the context."""
        event = create_event()
        response = self.client.get(reverse('major-event-log:event_details',
                                           args=[event.id]))
        # Check that the correct event is passed in the context.
        self.assertEqual(response.context['event'], event)

    def test_event_atom_content(self):
        """Check the content of the event_atom page.

        Contents are verified by checking that the proper event has
        been placed in the context and that the atom xml is well-
        formed."""
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
        # Check that the correct event is passed in the context.
        self.assertEqual(response.context['event'], event)
        # Make sure that the atom xml has the expected structure.
        atom = ET.fromstring(response.content)
        for xpath in expected_xml_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))

    def test_event_premis_content(self):
        """Check the content of the event_premis page.

        Contents are verified by checking that the proper event has
        been placed in the context and that the premis xml is well-
        formed."""
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
        # Check that the correct event is passed in the context.
        self.assertEqual(response.context['event'], event)
        # Make sure that the premis event has the expected structure.
        atom = ET.fromstring(response.content)
        for xpath in expected_premis_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))

    def test_feed_content(self):
        """Check that the feed creates a properly formed atom feed.

        Contents are verified by checking that only the most recent
        ten events have been placed in the context."""
        namespace = {'default': 'http://www.w3.org/2005/Atom'}
        expected_feed_structure = [
            './default:title',
            './default:link',
            './default:id',
            './default:updated',
            './default:subtitle',
            './default:entry'
        ]
        events = []
        for i in range(11):
            events.append(create_event())
        response = self.client.get(reverse('major-event-log:feed'))
        # Check that only the last ten events are passed in the context.
        self.assertNotContains(response, events[0].id)
        for event in events[1:]:
            self.assertContains(response, event.id)
        # Make sure that the premis event has the expected structure.
        atom = ET.fromstring(response.content)
        for xpath in expected_feed_structure:
            self.assertIsNotNone(atom.find(xpath, namespace))
