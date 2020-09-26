def pytest_configure(config):
    from config import Config
    Config.db_url += '_test'


def pytest_sessionstart(session):
    from models.utils import create_database_if_not_exists, drop_database_if_exists, alembic_upgrade_head
    from config import Config

    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
    create_database_if_not_exists()
    alembic_upgrade_head()


def pytest_sessionfinish(session):
    from models.utils import drop_database_if_exists
    from config import Config

    assert Config.db_url.endswith('_test')
    drop_database_if_exists()
