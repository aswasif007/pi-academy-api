from datetime import datetime
from unittest import TestCase
from tests.utils import db, create_mock_user, create_mock_event, create_mock_enrollment, teardown_data, get_test_client


class TestEventEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = create_mock_user(password='test')
        cls.enrollment = create_mock_enrollment(people=[cls.user])
        cls.events = [
            create_mock_event(enrollment=cls.enrollment),
            create_mock_event(user=cls.user),
            create_mock_event(),
            create_mock_event(user=create_mock_user()),
            create_mock_event(enrollment=create_mock_enrollment()),
        ]

        cls.client = get_test_client()
        resp = cls.client.post('/auth/login', json={'username': cls.user.username, 'password': 'test'})
        resp.raise_for_status()

        return super().setUpClass()
    
    def test_1_require_auth(self):
        client_not_logged_in = get_test_client()
        resp = client_not_logged_in.get('/events/')
        assert resp.status_code == 403

    def test_2_get_events(self):
        resp = self.client.get('/events/')
        assert resp.status_code == 200

        events = resp.json()
        assert len(events) == 3

    def test_3_create_event(self):
        data = {
            'subtitle': 'event-sub',
            'title': 'event-title',
            'type': 'test_result',
            'schedule': datetime.utcnow().isoformat(),
            'enrollment_guid': str(self.enrollment.guid),
        }

        resp = self.client.post('/events/', json=data)
        assert resp.status_code == 201

        event = resp.json()
        assert event['subtitle'] == data['subtitle']
        assert event['title'] == data['title']
        assert event['type'] == data['type']
        assert event['schedule'] == data['schedule']

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
