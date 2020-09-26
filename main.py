from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper

from config import Config
from models.utils import validate_database

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=Config.db_url)
validate_database()


@app.get('/')
def status():
    return {'status': 'online'}
