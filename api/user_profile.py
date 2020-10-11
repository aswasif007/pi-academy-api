from models import db, User, UserProfile, EntryDoesNotExist


def get(guid):
    profile = UserProfile.get_one(guid=guid)
    if not profile:
        raise EntryDoesNotExist

    return profile


def update(guid, data):
    profile = get(guid)
    profile.update(**data)
    db.session.commit()
    return profile
