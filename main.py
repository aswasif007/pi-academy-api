from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper

from config import Config
from models.utils import create_database_if_not_exists

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=Config.db_url)
create_database_if_not_exists()


@app.get('/')
def status():
    return {'status': 'online'}
