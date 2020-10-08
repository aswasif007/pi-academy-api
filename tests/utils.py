from datetime import datetime, timedelta
from faker import Faker
from models import db, User, Course, Enrollment
from fastapi.testclient import TestClient
from main import app


def create_mock_user(**kwargs):
    fake = Faker()
    user = User.create_one(
        name=kwargs.get('name', fake.name()),
        username=kwargs.get('username', fake.user_name()),
        password=kwargs.get('password', fake.password()),
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
    enrollment = Enrollment.create_one(
        course=create_mock_course(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=60),
        people=[create_mock_user(), create_mock_user()],
        status='open',
    )
    db.session.commit()
    return enrollment


test_client = TestClient(app)
