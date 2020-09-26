from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from config import Config


def validate_database():
    engine = create_engine(Config.db_url)
    if not database_exists(engine.url):
        create_database(engine.url)
