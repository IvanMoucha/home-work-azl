from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

from src.database.db import engine
from src.utils import logger

log = logger.get_logger(__name__)

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, index=True)
    description = Column(Text, index=True)
    link = Column(String(128))
    category = Column(String(128), index=True)
    pub_date = Column(DateTime, index=True)
    guid = Column(String(32), unique=True, index=True)
    media_thumbnail_url = Column(String(128))
    tldr = Column(Text, index=True)


def init():
    Base.metadata.create_all(engine)
    log.info("Initialized 'news' table.")
