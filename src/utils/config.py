import os

DATA_SOURCE = 'https://phys.org/rss-feed/'
DB_HOST = os.environ['DB_HOST'] if 'DB_HOST' in os.environ and os.environ['DB_HOST'] is not None else 'localhost'
DB_NAME = 'poc'
DB_USER = 'postgres'
DB_PASSWORD = 'mypassword'
DB_PORT = '5432'
REMOTE_LOCATION = 'file://tmp/'
