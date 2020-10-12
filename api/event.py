from models import db, Event, User


def get_user_events(user: User):
    enrollment_guids = [enrollment.guid for enrollment in user.enrollments]
    objs = db.session.query(Event).filter(
        (Event.enrollment_guid.is_(None) & Event.user_guid.is_(None)) |
        Event.enrollment_guid.in_(enrollment_guids) |
        Event.user_guid.in_([user.guid])
    )
    return [obj for obj in objs]


def create(data):
    obj = Event.create_one(**data)
    db.session.commit()
    return obj
