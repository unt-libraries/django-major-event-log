from django.utils import timezone
from django.test import TestCase

from .models import Event


class URLsToViewsTests(TestCase):
    """Tests to make sure that URLS get directed to the right views.

    Verifies that the correct information is captured from the urls,
    that the urls get directed correctly (or that the correct error
    is displayed), and that the correct templates get used.
    """

    def create_event(self, title='test', outcome='Success', name='John Doe'):
        """Create an event for testing."""
        if outcome == 'Success':
            outcome = 'http://purl.org/NET/UNTL/vocabularies/eventOutcomes/'\
                      '#success'
        else:
            outcome = 'http://purl.org/NET/UNTL/vocabularies/eventOutcomes/'\
                      '#failure'
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

    def test_valid_urls(self):
        """Check that valid URLs get directed to the correct views."""
        event_id = self.create_event().id
        urls = ['/major-event-log/',
                '/major-event-log/event/{}/'.format(event_id),
                '/major-event-log/event/{}.xml/'.format(event_id),
                '/major-event-log/event/{}.premis.xml/'.format(event_id),
                '/major-event-log/feed/',
                '/major-event-log/about/']
        responses = []
        for url in urls:
            responses.append(self.client.get(url))
        for response in responses:
            self.assertEqual(response.status_code, 200)

    def test_invalid_urls(self):
        """Check that invalid URL requests get an HTTP 404."""
        urls = ['/',
                '/nothing/',
                '/major-event-log/nothing/',
                '/major-event-log/event/',
                '/major-event-log/event/NOTHING/',
                '/major-event-log/feed/nothing/',
                '/major-event-log/about/nothing/']
        responses = []
        for url in urls:
            responses.append(self.client.get(url))
        for response in responses:
            self.assertEqual(response.status_code, 404)

    def test_invalid_uuids(self):
        """Check that uuid's that don't exist in the db are handled."""
        pass

    def test_url_uuid_catch(self):
        """Check that the uuid gets caught correctly by the regex."""
        pass

    def test_correct_templates_used(self):
        """Check that the right templates are used by the views."""
        pass


class ContentProducedTests(TestCase):
    """Tests to make sure contect is being produced correctly."""
    pass


class ModelInteractionTests(TestCase):
    """Tests that all interactions with the model proceed correctly."""
    pass
