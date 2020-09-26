from fastapi import FastAPI

from config import Config
from models import db_middleware
from models.utils import create_database_if_not_exists, alembic_upgrade_head

app = FastAPI()
app.middleware('http')(db_middleware)

create_database_if_not_exists()
alembic_upgrade_head()


@app.get('/')
def status():
    return {'status': 'online'}
