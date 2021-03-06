from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from alembic.config import Config as AlembicConfig
from alembic import command
from config import Config


def create_database_if_not_exists():
    engine = create_engine(Config.db_url)
    if not database_exists(engine.url):
        create_database(engine.url)


def drop_database_if_exists():
    engine = create_engine(Config.db_url)
    if database_exists(engine.url):
        drop_database(engine.url)


def alembic_upgrade_head():
    alembic_config = AlembicConfig('alembic.ini')
    command.upgrade(alembic_config, 'head')
