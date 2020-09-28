from unittest import TestCase

from datetime import datetime, timedelta
from models import db, Enrollment
from tests.utils import create_mock_user, create_mock_course


enrollment_data = [
    {
        'start_date': datetime.utcnow(),
        'end_date': datetime.utcnow() + timedelta(days=180),
    },
]

class TestEnrollment(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = [create_mock_user(), create_mock_user()]
        cls.courses = [create_mock_course(), create_mock_course()]
        return super().setUpClass()

    def test_create(self):
        enrollment = Enrollment.create_one(**enrollment_data[0], course=self.courses[0])
        db.session.commit()

        enrollment = Enrollment.get_one(guid=enrollment.guid)
        assert enrollment.status == 'open'
        assert enrollment.start_date == enrollment_data[0]['start_date']
        assert enrollment.end_date == enrollment_data[0]['end_date']
        assert enrollment.course.guid == self.courses[0].guid
        assert enrollment.people == []

    def test_update(self):
        enrollment = Enrollment.create_one(**enrollment_data[0], course=self.courses[0])
        db.session.commit()
        assert enrollment.status == 'open'

        enrollment.update(status='closed')
        db.session.commit()
        assert Enrollment.get_one(guid=enrollment.guid).status == 'closed'

    def test_delete(self):
        enrollment = Enrollment.get_one()
        enrollment.delete()
        db.session.commit()

        assert Enrollment.get_one(guid=enrollment.guid) == None

    def test_relationship__people(self):
        enrollment = Enrollment.create_one(**enrollment_data[0], course=self.courses[0])
        db.session.commit()

        assert enrollment.people == []

        enrollment.people.append(self.users[0])
        enrollment.people.append(self.users[1])
        db.session.commit()

        assert Enrollment.get_one(guid=enrollment.guid).people == self.users

        enrollment.people.remove(enrollment.people[0])
        db.session.commit()

        assert Enrollment.get_one(guid=enrollment.guid).people == [self.users[1]]

    def test_relationship__course(self):
        enrollment = Enrollment.create_one(**enrollment_data[0], course=self.courses[1])
        db.session.commit()

        assert enrollment.course == self.courses[1]
