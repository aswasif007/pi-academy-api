import threading

from uuid import uuid4

from contextvars import ContextVar
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
