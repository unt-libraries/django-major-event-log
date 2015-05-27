from django.core.urlresolvers import reverse, resolve
from django.utils import timezone
from django.test import TestCase

from .models import Event
from . import views


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
                '/major-event-log/event/nothing/',
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
        urls = ((reverse('major-event-log:index'),
                 views.index),
                (reverse('major-event-log:event_details', args=[uuid]),
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
        """Check the content of the index page."""
        event = create_event()
        # Dont know how to check that datetime is in the page, since format is
        # different.
        expected_values = [str(event.id), str(event.title),
                           'Event', 'Event Date', 'ID', 'Outcome']
        response = self.client.get(reverse('major-event-log:index'))
        for value in expected_values:
            self.assertContains(response, value)
        if 'success' in event.outcome:
            self.assertContains(response, 'Success')
        elif 'failure' in event.outcome:
            self.assertContains(response, 'Failure')

    def test_event_details_content(self):
        """Check the content of the event_details page."""
        event = create_event()
        # Don't know how to check that datetime is in the page, since format is
        # different.
        expected_values = [str(event.id), str(event.title), str(event.detail),
                           str(event.outcome_detail), str(event.contact_name),
                           str(event.contact_email), 'Title', 'Details', 'ID',
                           'Outcome', 'Outcome Details', 'Event Date',
                           'Created', 'Modified', 'Contact Name',
                           'Contact Email', 'ATOM', 'PREMIS XML']
        response = self.client.get(reverse('major-event-log:event_details',
                                           args=[event.id]))
        for value in expected_values:
            self.assertContains(response, value)
        if 'success' in event.outcome:
            self.assertContains(response, 'Success')
        elif 'failure' in event.outcome:
            self.assertContains(response, 'Failure')

    def test_event_atom_content(self):
        """Check the content of the event_atom page."""
        pass

    def test_event_premis_content(self):
        """Check the content of the event_premis page."""
        pass

    def test_feed_content(self):
        """Check the content of the feed page."""
        pass

    def test_about_content(self):
        """Check the content of the about page."""
        pass


class TestModelInteraction(TestCase):
    """Tests that all interactions with the model proceed correctly."""

    def test_missing_info_rejected(self):
        """Check that db entries with missing info are rejected."""
        pass

    def test_good_info_accepted(self):
        """Check that db entries with all info present are accepted."""
        pass

    def test_stored_info_same_as_entered(self):
        """Check that what was entered was stored correctly."""
        pass

    def test_modified_info_saved_correctly(self):
        """Check that modified info is stored correctly."""
        pass
