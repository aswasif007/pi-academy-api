from unittest import TestCase
from models import Course
from tests.utils import create_mock_user, create_mock_course, teardown_data, get_test_client
from main import app


class TestCourseEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = get_test_client()
        cls.client_not_logged_in = get_test_client()

        user = create_mock_user(password='test')
        cls.client.post('/auth/login', json={'username': user.username, 'password': 'test'})
        cls.courses = [create_mock_course(), create_mock_course()]

        return super().setUpClass()

    def test_get_course(self):
        resp = self.client.get(f'/courses/{self.courses[1].guid}')
        assert resp.status_code == 200

        course = resp.json()
        assert course['code'] == self.courses[1].code
        assert course['title'] == self.courses[1].title
        assert course['description'] == self.courses[1].description
        assert course['outlines'] == self.courses[1].outlines
        assert course['tags'] == self.courses[1].tags
        assert course['takeaways'] == self.courses[1].takeaways

        assert self.client_not_logged_in.get(f'/courses/{self.courses[1].guid}').status_code == 403

    def test_get_all_courses(self):
        resp = self.client.get('/courses/')
        assert resp.status_code == 200

        courses = resp.json()
        assert len(courses) == len(self.courses)

        assert self.client_not_logged_in.get('/courses/').status_code == 403

    def test_add_new_course(self):
        payload = {'code': 'TST-12', 'title': 'test-title', 'description': 'test-desc', 'outlines': ['first', 'sec'], 'tags': ['tag1'], 'takeaways': []}
        resp = self.client.post('/courses/', json=payload)
        assert resp.status_code == 201

        course = resp.json()
        assert course['code'] == payload['code']
        assert course['title'] == payload['title']
        assert course['description'] == payload['description']
        assert course['outlines'] == payload['outlines']
        assert course['tags'] == payload['tags']
        assert course['takeaways'] == payload['takeaways']

        assert self.client_not_logged_in.post('/courses/', json=payload).status_code == 403

    def test_delete_course(self):
        resp = self.client.delete(f'/courses/{self.courses[0].guid}')
        assert resp.status_code == 204

        assert Course.get_one(guid=self.courses[0].guid) is None

        assert self.client_not_logged_in.delete(f'/courses/{self.courses[0].guid}').status_code == 403

    def test_update_course(self):
        payload = {'description': 'this is updated'}
        resp = self.client.patch(f'/courses/{self.courses[1].guid}', json=payload)
        assert resp.status_code == 200

        course = resp.json()
        assert course['description'] == payload['description']

        assert self.client_not_logged_in.delete(f'/courses/{self.courses[0].guid}').status_code == 403

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
