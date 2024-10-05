from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem
from src.database.db import engine
from src.database.m_news import News

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

def get_news_by_guid(guid):
    """
    Retrieve a news item from the database based on the provided GUID.

    Args:
        guid (str): The GUID of the news item to retrieve.

    Returns:
        News: The News object if found, None otherwise.
    """
    session = Session()
    try:
        news_item = session.query(News).filter(News.guid == guid).first()
        return news_item
    except SQLAlchemyError as e:
        log.error("Error retrieving news item with GUID %s: %s", guid, e)
        raise e
    finally:
        session.close()

def get_all_news():
    """
    Retrieve all news items from the database.

    Returns:
        List[News]: A list of all News objects in the database.
    """
    session = Session()
    try:
        news_items = session.query(News).all()
        return news_items
    except SQLAlchemyError as e:
        log.error("Error retrieving all news items: %s", e)
        raise e
    finally:
        session.close()

def search_news(query):
    """
    Search for news items in the database based on the provided query.

    Args:
        query (str): The search query.

    Returns:
        List[News]: A list of News objects that match the search query.
    """
    session = Session()
    try:
        search_query = f"%{query}%"
        news_items = session.query(News).filter(
            (News.title.ilike(search_query)) |
            (News.description.ilike(search_query)) |
            (News.category.ilike(search_query)) |
            (News.tldr.ilike(search_query))
        ).all()
        return news_items
    except SQLAlchemyError as e:
        log.error("Error searching news items with query %s: %s", query, e)
        raise e
    finally:
        session.close()