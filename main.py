from fastapi import FastAPI, Depends
from models import db_middleware
from routes import auth, courses, discussions, profiles, enrollments, events
from api import auth as authAPI
from openapi import get_openapi

app = FastAPI()
app.middleware('http')(db_middleware)
app.openapi = get_openapi(app)

authorization = Depends(authAPI.is_authorized)

@app.get('/')
def status():
    return {'status': 'online'}


app.include_router(auth, prefix='/auth', tags=['Auth'])
app.include_router(courses, prefix='/courses', dependencies=[authorization], tags=['Courses'])
app.include_router(discussions, prefix='/discussions', dependencies=[authorization], tags=['Discussions'])
app.include_router(profiles, prefix='/profiles', dependencies=[authorization], tags=['Profiles'])
app.include_router(enrollments, prefix='/enrollments', dependencies=[authorization], tags=['Enrollments'])
app.include_router(events, prefix='/events', dependencies=[authorization], tags=['Events'])
