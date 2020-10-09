import pytest

from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from models import Course, db
from tests.utils import teardown_data

course_data = [
    {
        "code": "CS-101",
        "title": "The Demo",
        "description": "This is a demo course",
        "takeaways": ["CS Knowledge", "Intro"],
        "tags": ["cs"],
        "outlines": [],
    },
    {
        "code": "UI-104",
        "title": "Another Demo",
        "description": "This is another demo course",
        "takeaways": ["UI", "Advanced"],
        "tags": [],
        "outlines": ["Learn advanced UI"],
    }
]


class TestCourse(TestCase):
    def test_add(self):
        course = Course.create_one(**course_data[0])
        db.session.commit()

        course = Course.get_one(guid=course.guid)
        assert course is not None
        assert course.code == course_data[0]['code']
        assert course.title == course_data[0]['title']
        assert course.description == course_data[0]['description']
        assert course.takeaways == course_data[0]['takeaways']
        assert course.tags == course_data[0]['tags']
        assert course.outlines == course_data[0]['outlines']

    def test_update(self):
        Course.create_one(**course_data[1])
        db.session.commit()

        Course.get_one(code=course_data[1]['code']).update(description='Updated description.')
        db.session.commit()

        assert Course.get_one(code=course_data[1]['code']).description == 'Updated description.'

    def test_delete(self):
        Course.get_one(code=course_data[0]['code']).delete()
        db.session.commit()

        assert Course.get_one(code=course_data[0]['code']) is None

    def test_code_uniqueness(self):
        Course.create_one(code=course_data[0]['code'], title='test', description='test')

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
