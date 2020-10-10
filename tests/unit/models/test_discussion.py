from unittest import TestCase
from uuid import uuid4
from tests.utils import create_mock_user, create_mock_enrollment, create_mock_discussion, teardown_data
from models import db, Discussion


discussion_data = [
    {
        'body': 'that the quick brown fox',
    },
    {
        'body': 'jumps over the lazy dog.'
    }
]

class TestDiscussion(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.discussion_guid = uuid4()
        cls.users = [create_mock_user(), create_mock_user()]
        cls.enrollments = [create_mock_enrollment(), create_mock_enrollment()]
        return super().setUpClass()

    def test_create(self):
        discussion = Discussion.create_one(**discussion_data[0], guid=self.discussion_guid, author=self.users[0], enrollment=self.enrollments[0])
        db.session.commit()

        discussion = Discussion.get_one(guid=discussion.guid)
        assert discussion is not None
        assert discussion.body == discussion_data[0]['body']
        assert discussion.author == self.users[0]
        assert discussion.enrollment == self.enrollments[0]

    def test_update(self):
        discussion = Discussion.create_one(**discussion_data[1], author=self.users[1])
        db.session.commit()

        assert discussion.enrollment != self.enrollments[0]

        discussion.update(enrollment=self.enrollments[0])
        db.session.commit()

        assert Discussion.get_one(guid=discussion.guid).enrollment == self.enrollments[0]

    def test_delete(self):
        Discussion.get_one(guid=self.discussion_guid).delete()
        db.session.commit()
        assert Discussion.get_one(guid=self.discussion_guid) is None

    def test_create__post_and_comments(self):
        post = create_mock_discussion()
        comments = [create_mock_discussion(post=post), create_mock_discussion(post=post)]

        assert post.comments == comments
        assert all([com.post == post for com in comments]) is True

    @classmethod
    def tearDownClass(cls):
        teardown_data()
        return super().tearDownClass()
