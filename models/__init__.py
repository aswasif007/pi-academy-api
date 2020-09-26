import threading

from datetime import datetime
from uuid import uuid4

from contextvars import ContextVar
from fastapi_utils.guid_type import GUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_wrapper import SQLAlchemy
from config import Config


context_id = ContextVar('context_id', default='')


class FastAPISQLAlchemy(SQLAlchemy):
    def _create_scoped_session(self, **kwargs):
        global context_id

        try:
            import fastapi  # noqa
        except ImportError:
            scopefunc = threading.get_ident
        else:
            scopefunc = context_id.get

        session = sessionmaker(**kwargs)
        return scoped_session(session, scopefunc=scopefunc)


db = FastAPISQLAlchemy(Config.db_url)


async def db_middleware(request, call_next):
    token = context_id.set(uuid4().hex)
    try:
        response = await call_next(request)
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.remove()
        context_id.reset(token)

    return response


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    guid = Column(GUID, primary_key=True, default=uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower() + 's'

    @classmethod
    def get_one(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def create_one(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        return obj

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise f'Invalid property {k}'

    def delete(self):
        db.session.delete(self)


from .course import Course
