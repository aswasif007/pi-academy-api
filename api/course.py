from models import db, Course, EntryDoesNotExist


def get(guid):
    obj = Course.get_one(guid=guid)
    if not obj:
        raise EntryDoesNotExist

    return obj.to_dict()


def get_all():
    objs = Course.get_all()
    return [obj.to_dict() for obj in objs]


def create(data):
    course = Course.create_one(**data)
    db.session.commit()

    return course.to_dict()


def delete(guid):
    course = Course.get_one(guid=guid)
    if not course:
        raise EntryDoesNotExist

    course.delete()
    db.session.commit()


def update(guid, data):
    course = Course.get_one(guid=guid)
    if not course:
        raise EntryDoesNotExist

    course.update(**data)
    db.session.commit()

    return course.to_dict()
