import os

class Config(object):
    db_url = 'postgres://{0[DB_USER]}:{0[DB_PASS]}@{0[DB_HOST]}:{0[DB_PORT]}/{0[DB_NAME]}'.format(os.environ)
