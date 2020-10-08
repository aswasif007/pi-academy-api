from unittest import TestCase
from tests.utils import create_mock_user, test_client


class TestAuthEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = create_mock_user(username='mock_user', password='pswd');
        return super().setUpClass()

    def test_login__valid_cred(self):
        resp = test_client.post('/auth/login', json={'username': 'mock_user', 'password': 'pswd'})
        assert resp.status_code == 200

        data = resp.json()
        assert data['access_token'] is not None
        assert data['token_type'] == 'bearer'

    def test_login__invalid_cred(self):
        resp = test_client.post('/auth/login', json={'username': 'mock_user', 'password': 'pswd_w'})
        assert resp.status_code == 401

    def test_logout(self):
        resp = test_client.post('/auth/logout')
        assert resp.status_code == 200

    def test_get_current_user__logged_in(self):
        test_client.post('/auth/login', json={'username': 'mock_user', 'password': 'pswd'})
        resp = test_client.get('/auth/current-user')
        assert resp.status_code == 200
        
        data = resp.json()
        assert data['guid'] == str(self.user.guid)
        assert data['name'] == self.user.name
        assert data['username'] == self.user.username
        assert data['category'] == self.user.category
        assert data['avatar'] == self.user.avatar

    def test_get_current_user__not_logged_in(self):
        test_client.post('/auth/logout')
        resp = test_client.get('/auth/current-user')
        assert resp.status_code == 403
