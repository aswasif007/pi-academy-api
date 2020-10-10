from unittest import TestCase
from models import Discussion
from tests.utils import get_test_client, create_mock_user, create_mock_discussion_thread


class TestDiscussionEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = [create_mock_user(password='test'), create_mock_user()]
        cls.threads = [create_mock_discussion_thread(), create_mock_discussion_thread()]

        cls.client = get_test_client()
        resp = cls.client.post('/auth/login', json={'username': cls.users[0].username, 'password': 'test'})
        resp.raise_for_status()

        return super().setUpClass()

    def test_require_auth(self):
        client_not_logged_in = get_test_client()
        assert client_not_logged_in.get('/discussions/').status_code == 403

    def test_1_get_threads(self):
        resp = self.client.get('/discussions/')
        assert resp.status_code == 200

        threads = resp.json()
        assert len(threads) == 2

        for i, thread in enumerate(threads):
            assert thread['guid'] == str(self.threads[i].guid)
            assert thread['post']['body'] == self.threads[i].body
            assert thread['post']['author']['guid'] == str(self.threads[i].author_guid)
            for j, comment in enumerate(thread['comments']):
                assert comment['guid'] == str(self.threads[i].comments[j].guid)
                assert comment['body'] == self.threads[i].comments[j].body
                assert comment['author']['guid'] == str(self.threads[i].comments[j].author_guid)

    def test_2_create_thread(self):
        resp = self.client.post(f'/discussions/', json={'body': 'post-body'})
        assert resp.status_code == 201

        thread = resp.json()
        assert thread['post']['body'] == 'post-body'
        assert thread['comments'] == []
        assert thread['post']['author']['guid'] == str(self.users[0].guid)

    def test_3_delete_discussion(self):
        resp = self.client.delete(f'/discussions/{self.threads[1].guid}')
        assert resp.status_code == 204
        assert Discussion.get_one(guid=self.threads[1].guid) is None

    def test_4_add_comment(self):
        resp = self.client.post(f'/discussions/{self.threads[0].guid}/comments', json={'body': 'comment-body'})
        assert resp.status_code == 201

        comment = resp.json()
        assert comment['body'] == 'comment-body'
        assert comment['author']['guid'] == str(self.users[0].guid)

    @classmethod
    def tearDownClass(cls):
        return super().tearDownClass()
