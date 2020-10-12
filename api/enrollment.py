from models import db, Enrollment


def get(guid):
    return Enrollment.get_one(guid=guid)
