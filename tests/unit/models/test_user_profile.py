from unittest import TestCase
from models import db, UserProfile
from tests.utils import create_mock_user, teardown_data

profile_data = [
    {
        'bio': 'this is my bio',
        'email': 'themail@mail.com',
        'interests': ['Python', 'JS'],
    }
]


class TestUserProfile(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = [create_mock_user(), create_mock_user()]
        return super().setUpClass()

    def test_create(self):
        UserProfile.create_one(**profile_data[0], user=self.users[0])
        db.session.commit()

        profile = UserProfile.get_one(guid=self.users[0].guid)
        assert profile is not None
        assert profile.bio == profile_data[0]['bio']
        assert profile.email == profile_data[0]['email']
        assert profile.interests == profile_data[0]['interests']
        assert profile.user.guid == self.users[0].guid

    def test_update(self):
        UserProfile.create_one(**profile_data[0], user=self.users[1])
        db.session.commit()

        UserProfile.get_one(guid=self.users[1].guid).update(bio='update-bio')
        db.session.commit()

        assert UserProfile.get_one(guid=self.users[1].guid).bio == 'update-bio'

    def test_delete(self):
        UserProfile.get_one(guid=self.users[0].guid).delete()
        db.session.commit()

        assert UserProfile.get_one(guid=self.users[0].guid) is None

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
