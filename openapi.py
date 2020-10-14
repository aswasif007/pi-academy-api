from fastapi.openapi.utils import get_openapi as get_openapi_base


tags = [
    {
        'name': 'Auth',
        'description': '''
        \nPi Academy API relies on OAuth2 for authorization. The auth token is read from request cookie. The following set of
        endpoints take care of login related stuffs.
        '''
    },
    {
        'name': 'Courses',
        'description': '''
        \nThis set of endpoints are for listing, adding and removing courses to the database. A course can be added/removed by a
        *Curator*. However, all the users can read the course list.
        '''
    },
    {
        'name': 'Discussions',
        'description': '''
        \nDiscussions are mainly conversation threads. But each post and comment is considered a single discussion.
        This set of endpoints are responsible for listing, adding, deleting and updating threads, posts and comments.
        '''
    },
    {
        'name': 'Enrollments',
        'description': '''
        \nAn *enrollment* is an instance of a course. Each enrollment has a limited timeframe and a closed boundary consisting of a
        set of users. There are two types of users in an enrollment:
        \n- Professors
        \n- Students
        \nProfessors are considered admins of the enrollment. They can add/remove users as well as post notices and moderate conversations.
        '''
    },
    {
        'name': 'Events',
        'description': '''
        \nThere are three types of events:
        \n- **Notice**: To informs audiences a general info across the platform.
        \n- **Test**: To inform students of an enrollment about an upcoming exam. Enrollment specific event.
        \n- **Test Result**: To inform a student the outcome of a past exam. User specific event.
        '''
    },
    {
        'name': 'Profiles',
        'description': '''
        \nThese set of endpoints serve profile of a user, as well as update logged-in user's info.
        '''
    }
]

def get_openapi(app):
    def openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi_base(
            title='Pi Academy API',
            description='''
            \n# Introduction
            \nA RESTFul API for **Pi Academy** project. Built with love, as well as FastAPI and PostgreSQL.
            ''',
            version='1.0.0',
            routes=app.routes,
            tags=tags,
        )
        openapi_schema['info']['x-logo'] = {'url': './icon.svg'}
        openapi_schema['x-tagGroups'] = [{'name': 'General', 'tags': ['Auth', 'Courses', 'Discussions', 'Enrollments', 'Events', 'Profiles']}]
        app.openapi_schema = openapi_schema

        return app.openapi_schema

    return openapi
