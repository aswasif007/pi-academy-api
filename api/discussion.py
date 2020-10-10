from models import db, Discussion, EntryDoesNotExist


def get(guid):
    obj = Discussion.get_one(guid=guid)
    if not obj:
        raise EntryDoesNotExist

    return obj


def get_general_posts():
    objs = db.session.query(Discussion).filter(Discussion.enrollment_guid.is_(None), Discussion.post_guid.is_(None))
    return [obj for obj in objs]


def create(data):
    post_guid = data.pop('post_guid', None)
    data['post'] = post_guid and get(post_guid)
    obj = Discussion.create_one(**data)
    db.session.commit()

    return obj


def delete(guid):
    obj = get(guid)
    obj.delete()
    db.session.commit()
