from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.data_pipeline.c_newsitem import NewsItem
from src.database.m_news import News
from src.database.db import engine
import src.utils.logger as logger


log = logger.get_logger(__name__)

# Create a session factory
Session = sessionmaker(bind=engine)

def guid_exists(guid):
    """
    Check if a news item with the given guid exists in the database.

    Args:
        guid (str): The GUID to check.

    Returns:
        bool: True if the GUID exists, False otherwise.
    """
    session = Session()
    try:
        exists = session.query(News).filter(News.guid == guid).first() is not None
        return exists
    finally:
        session.close()

def insert_news_item(news_item: NewsItem):
    """
    Convert NewsItem to News and insert it into the database.

    Args:
        news_item (NewsItem): The News object to insert.

    Returns:
        None
    """
    news = News(guid=news_item.guid,
                title=news_item.title,
                description=news_item.description,
                link=news_item.link,
                category=news_item.category,
                pub_date=news_item.pub_date,
                media_thumbnail_url=news_item.media_thumbnail_url,
                tldr=news_item.tldr)
    insert_news(news)

def insert_news(news: News):
    """
    Inserts a new News item into the database.

    Args:
        news (News): The News object to insert.

    Returns:
        None
    """
    session = Session()
    try:
        session.add(news)
        session.commit()
        log.info("Inserted news item with GUID: %s", news.guid)
    except SQLAlchemyError as e:
        session.rollback()
        log.error("Error inserting news item with GUID %s: %s", news.guid, e)
        raise e
    finally:
        session.close()

def update_news_item(news_item: NewsItem):
    """
    Convert NewsItem to News and update it in the database.

    Args:
        news_item (NewsItem): The News object to insert.

    Returns:
        None
    """
    news = News(guid=news_item.guid,
                title=news_item.title,
                description=news_item.description,
                link=news_item.link,
                category=news_item.category,
                pub_date=news_item.pub_date,
                media_thumbnail_url=news_item.media_thumbnail_url,
                tldr=news_item.tldr)
    update_news(news)

def update_news(news_item: News):
    """
    Updates an existing News item in the database.

    Args:
        news_item (News): The News object with updated data.

    Returns:
        None
    """
    session = Session()
    try:
        existing_news = session.query(News).filter(News.guid == news_item.guid).first()
        if existing_news:
            # Update fields
            existing_news.title = news_item.title
            existing_news.description = news_item.description
            existing_news.link = news_item.link
            existing_news.category = news_item.category
            existing_news.pub_date = news_item.pub_date
            existing_news.media_thumbnail_url = news_item.media_thumbnail_url
            existing_news.tldr = news_item.tldr
            session.commit()
            log.info("Updated news item with GUID: %s", news_item.guid)
        else:
            log.warning("News item with GUID %s does not exist. No update performed.", news_item.guid)
    except SQLAlchemyError as e:
        session.rollback()
        log.error("Error updating news item with GUID %s: %s", news_item.guid, e)
        raise e
    finally:
        session.close()