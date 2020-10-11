from unittest import TestCase
from tests.utils import get_test_client, create_mock_user, create_mock_user_profile, teardown_data


class TestProfileEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = create_mock_user(password='test')
        cls.profiles = [create_mock_user_profile(user=cls.user), create_mock_user_profile()]

        cls.test_client = get_test_client()
        resp = cls.test_client.post('/auth/login', json={'username': cls.user.username, 'password': 'test'})
        resp.raise_for_status()

        return super().setUpClass()

    def test_require_auth(self):
        client_not_logged_in = get_test_client()
        resp = client_not_logged_in.get(f'/profiles/{self.user.guid}')
        assert resp.status_code == 403

    def test_get_user_profile(self):
        resp = self.test_client.get(f'/profiles/{self.profiles[1].guid}')
        assert resp.status_code == 200

        profile = resp.json()
        assert profile['guid'] == str(self.profiles[1].guid)
        assert profile['bio'] == self.profiles[1].bio
        assert profile['email'] == self.profiles[1].email
        assert profile['interests'] == self.profiles[1].interests

    def test_get_current_user_profile(self):
        resp = self.test_client.get('/profiles/current-user')
        assert resp.status_code == 200

        profile = resp.json()
        assert profile['guid'] == str(self.profiles[0].guid)
        assert profile['bio'] == self.profiles[0].bio
        assert profile['email'] == self.profiles[0].email
        assert profile['interests'] == self.profiles[0].interests

    def test_update_current_user_profile(self):
        resp = self.test_client.patch('/profiles/current-user', json={'bio': 'updated-bio'})
        assert resp.status_code == 200

        profile = resp.json()
        assert profile['bio'] == 'updated-bio'

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
