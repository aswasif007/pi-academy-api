from config import Config
from models.utils import create_database_if_not_exists, drop_database_if_exists
from alembic.config import Config as AlembicConfig
from alembic import command


def pytest_configure(config):
    Config.db_url += '_test'


def pytest_sessionstart(session):
    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
    create_database_if_not_exists()

    alembic_config = AlembicConfig('alembic.ini')
    command.upgrade(alembic_config, 'head')

def pytest_sessionfinish(session):
    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
