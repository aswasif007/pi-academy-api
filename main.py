from fastapi import FastAPI
from models import db_middleware

app = FastAPI()
app.middleware('http')(db_middleware)


@app.get('/')
def status():
    return {'status': 'online'}
