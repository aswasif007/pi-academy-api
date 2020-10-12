from unittest import TestCase
from tests.utils import db, create_mock_enrollment, create_mock_user, create_mock_discussion_thread, get_test_client, teardown_data


class TestEnrollmentEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = create_mock_user(password='test')
        people = [create_mock_user(category='professor'), create_mock_user(), cls.user]
        cls.enrollments = [create_mock_enrollment(people=people), create_mock_enrollment(people=people), create_mock_enrollment()]
        cls.threads = [
            create_mock_discussion_thread(enrollment=cls.enrollments[0]),
            create_mock_discussion_thread(enrollment=cls.enrollments[0]),
            create_mock_discussion_thread(enrollment=cls.enrollments[1]),
        ]

        cls.client = get_test_client()
        resp = cls.client.post('/auth/login', json={'username': cls.user.username, 'password': 'test'})
        resp.raise_for_status()

        return super().setUpClass()

    def test_1_require_auth(self):
        client_not_logged_in = get_test_client()
        resp = client_not_logged_in.get('/enrollments/')
        assert resp.status_code == 403

    def test_2_get_all_enrollments(self):
        resp = self.client.get('/enrollments/')
        assert resp.status_code == 200

        enrollments = resp.json()
        assert len(enrollments) == 2
        for i, enrollment in enumerate(enrollments):
            assert enrollment['guid'] == str(self.enrollments[i].guid)
            assert enrollment['code'] == self.enrollments[i].course.code
            assert enrollment['title'] == self.enrollments[i].course.title
    
    def test_3_get_enrollment_details(self):
        resp = self.client.get(f'/enrollments/{self.enrollments[0].guid}/details')
        assert resp.status_code == 200

        enrollment_details = resp.json()
        assert enrollment_details['guid'] == str(self.enrollments[0].guid)
        assert enrollment_details['status'] == self.enrollments[0].status
        assert len(enrollment_details['instructors']) == 1
        assert len(enrollment_details['members']) == 2
    
    def test_4_get_enrollment_threads(self):
        resp = self.client.get(f'/enrollments/{self.enrollments[0].guid}/discussions')
        assert resp.status_code == 200

        threads = resp.json()
        assert len(threads) == 2
        for i, thread in enumerate(threads):
            assert thread['guid'] == str(self.threads[i].guid)

    def test_5_get_enrollment_threads__not_enrolled_user(self):
        resp = self.client.get(f'/enrollments/{self.enrollments[2].guid}/discussions')
        assert resp.status_code == 404

    def test_6_get_enrollment_details__not_enrolled_user(self):
        resp = self.client.get(f'/enrollments/{self.enrollments[2].guid}/details')
        assert resp.status_code == 404

    def test_7_create_enrollment_thread(self):
        resp = self.client.post(f'/enrollments/{self.enrollments[1].guid}/discussions', json={'body': 'hello world'})
        assert resp.status_code == 201

        thread = resp.json()
        assert thread['post']['body'] == 'hello world'
        assert thread['comments'] == []

    def test_8_create_enrollment_thread__not_enrolled_user(self):
        resp = self.client.post(f'/enrollments/{self.enrollments[2].guid}/discussions', json={'body': 'hello world'})
        assert resp.status_code == 404

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
