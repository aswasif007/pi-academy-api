from datetime import datetime, timedelta
from faker import Faker
from models import db, User, Course, Enrollment, Discussion, Event, UserProfile
from fastapi.testclient import TestClient
from main import app


def create_mock_user(**kwargs):
    fake = Faker()
    user = User.create_one(
        name=kwargs.get('name', fake.name()),
        username=kwargs.get('username', fake.user_name()),
        password=kwargs.get('password', fake.password()),
        category=kwargs.get('category', 'student'),
        avatar=fake.uri(),
    )
    db.session.commit()
    return user


def create_mock_course(**kwargs):
    fake = Faker()
    course = Course.create_one(
        code=fake.word(),
        title=fake.sentence(),
        description=fake.sentence(),
        outlines=fake.sentences(),
        tags=fake.words(),
        takeaways=fake.sentences(),
    )
    db.session.commit()
    return course


def create_mock_enrollment(**kwargs):
    people = kwargs.pop('people', [create_mock_user(), create_mock_user()])
    enrollment = Enrollment.create_one(
        course=create_mock_course(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=60),
        status='open',
    )
    for user in people:
        enrollment.people.append(user)

    db.session.commit()
    return enrollment


def create_mock_discussion(**kwargs):
    fake = Faker()
    discussion = Discussion.create_one(
        body=fake.sentences(),
        author=kwargs.get('author', create_mock_user()),
        enrollment=kwargs.get('enrollment'),
        post=kwargs.get('post'),
    )
    db.session.commit()
    return discussion


def create_mock_discussion_thread(**kwargs):
    post = create_mock_discussion(**kwargs)
    comments = kwargs.pop('comments', [create_mock_discussion(), create_mock_discussion()])
    for comment in comments:
        comment.post = post
    
    db.session.commit()
    return post


def create_mock_user_profile(**kwargs):
    fake = Faker()
    profile = UserProfile.create_one(
        user=kwargs.get('user', create_mock_user()),
        bio=fake.sentences(),
        email=fake.email(),
        interests=[fake.word(), fake.word()],
    )
    db.session.commit()
    return profile


def teardown_data():
    for model in [User, Course, Enrollment, Event, Discussion, UserProfile]:
        db.session.query(model).delete()

    db.session.commit()


def get_test_client():
    return TestClient(app)
