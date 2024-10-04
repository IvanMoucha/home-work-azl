from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import src.utils.config as config
import src.utils.logger as logger


log = logger.get_logger(__name__)

# Construct the database URL
DATABASE_URL = f'postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

# Create an engine with a connection pool
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=20,  # Allows up to 25 connections in total (5 + 20)
    poolclass=QueuePool
)

def get_connection():
    return engine.connect()

def close_connection(connection):
    connection.close()

def init() :    # Test the connection
    try:
        with get_connection() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()
            log.info("Connected to DB - %s", version[0])
    except Exception as e:
        log.error("Error while connecting to the database: %s", e)
        raise (e)