from fastapi import FastAPI, Depends
from models import db_middleware
from routes import auth, courses
from api import auth as authAPI

app = FastAPI()
app.middleware('http')(db_middleware)

authorization = Depends(authAPI.is_authorized)

@app.get('/')
def status():
    return {'status': 'online'}


app.include_router(auth, prefix='/auth')
app.include_router(courses, prefix='/courses', dependencies=[authorization])
