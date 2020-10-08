from fastapi import FastAPI
from models import db_middleware
from routes import auth

app = FastAPI()
app.middleware('http')(db_middleware)


@app.get('/')
def status():
    return {'status': 'online'}


app.include_router(auth, prefix='/auth')
