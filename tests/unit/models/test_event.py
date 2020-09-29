from uuid import uuid4
from datetime import datetime
from unittest import TestCase
from tests.utils import create_mock_enrollment, create_mock_user
from models import db, Event

event_data = [
    {
        'subtitle': 'this is subtitle',
        'title': 'this is title',
        'type': 'notice',
        'schedule': datetime.utcnow(),
    }
]

class TestEvent(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.event_guid = uuid4()
        cls.users = [create_mock_user(), create_mock_user()]
        cls.enrollments = [create_mock_enrollment(), create_mock_enrollment()]
        return super().setUpClass()

    def test_create(self):
        Event.create_one(**event_data[0], guid=self.event_guid, user=self.users[0], enrollment=self.enrollments[0])
        db.session.commit()

        event = Event.get_one(guid=self.event_guid)
        assert event is not None
        assert event.subtitle == event_data[0]['subtitle']
        assert event.title == event_data[0]['title']
        assert event.type == event_data[0]['type']
        assert event.schedule == event_data[0]['schedule']
        assert event.user == self.users[0]
        assert event.enrollment == self.enrollments[0]

    def test_update(self):
        event = Event.create_one(**event_data[0])
        db.session.commit()

        event.update(subtitle='changed subtitle')
        db.session.commit()

        assert Event.get_one(guid=event.guid).subtitle == 'changed subtitle'

    def test_delete(self):
        Event.get_one(guid=self.event_guid).delete()
        db.session.commit()

        assert Event.get_one(guid=self.event_guid) is None
