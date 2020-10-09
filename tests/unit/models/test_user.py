import pytest

from unittest import TestCase
from models import db, User
from sqlalchemy.exc import IntegrityError
from tests.utils import teardown_data

user_data = [
    {
        "name": "Doe",
        "username": "doe_u",
        "password": "doe_p",
        "category": "professor",
    },
    {
        "name": "Boo",
        "username": "boofe",
        "password": "boofee",
    },
]


class TestUser(TestCase):
    def test_create(self):
        User.create_one(**user_data[0])
        db.session.commit()

        user = User.get_one(username='doe_u')
        assert user is not None
        assert user.name == user_data[0]['name']
        assert user.username == user_data[0]['username']
        assert user.category == user_data[0]['category']
        assert user.avatar == None

        with pytest.raises(Exception):
            user.password

    def test_create__default_category(self):
        User.create_one(**user_data[1])
        db.session.commit()

        user = User.get_one(username='boofe')
        assert user is not None
        assert user.category == 'student'

    def test_update(self):
        User.get_one(username='doe_u').update(name='John Doe')
        db.session.commit()

        assert User.get_one(username='doe_u').name == 'John Doe'

    def test_delete(self):
        User.get_one(username='boofe').delete()
        db.session.commit()

        assert User.get_one(username='boofe') is None

    def test_username_uniqueness(self):
        User.create_one(name='Bar', username=user_data[0]['username'], password='bar')
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

    def test_validate_password(self):
        user = User.get_one(username = user_data[0]['username'])
        assert user.validate_password(user_data[0]['password']) is True
        assert user.validate_password('wrongpass') is False

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
