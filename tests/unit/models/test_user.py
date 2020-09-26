from unittest import TestCase
from models import db, User

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
        assert user.password == user_data[0]['password']
        assert user.category == user_data[0]['category']
        assert user.avatar == None

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
