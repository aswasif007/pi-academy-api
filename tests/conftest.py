from config import Config
from models.utils import create_database_if_not_exists, drop_database_if_exists


def pytest_configure(config):
    Config.db_url += '_test'


def pytest_sessionstart(session):
    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
    create_database_if_not_exists()


def pytest_sessionfinish(session):
    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
