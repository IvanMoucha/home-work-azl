import os

DATA_SOURCE = 'https://phys.org/rss-feed/'
DB_HOST = os.environ['DB_HOST'] if 'DB_HOST' in os.environ and os.environ['DB_HOST'] is not None else 'localhost'
DB_NAME = 'poc'
DB_USER = 'postgres'
DB_PASSWORD = 'mypassword'
DB_PORT = '5432'
REMOTE_LOCATION = 'file://tmp/'

LLM = True if 'LLM' in os.environ and os.environ['LLM'] == "1" else False
LLM_MODEL = "unsloth/Llama-3.2-1B-Instruct"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

