import os

class Config(object):
    db_url = 'postgres://{0[DB_USER]}:{0[DB_PASS]}@postgres:5432/pi_academy'.format(os.environ)
