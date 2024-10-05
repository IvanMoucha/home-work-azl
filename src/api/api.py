from typing import List

from fastapi import APIRouter, HTTPException

import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem
from src.database import db, dao_news

log = logger.get_logger(__name__)

db.init()

router = APIRouter()


@router.get("/news", response_model=List[NewsItem], tags=["news"])
def list_news():
    """List all news items."""
    return dao_news.get_all_news()


@router.get("/news/search", response_model=List[NewsItem], tags=["news"])
def search_news(q: str):
    """Search news items by specific text."""
    log.info(f"Searching for news items with query: {q}")
    return dao_news.search_news(q)


@router.get("/news/{id}", response_model=NewsItem, tags=["news"])
def get_news(id: str):
    """Retrieve a specific news item by ID."""
    news_item = dao_news.get_news_by_guid(id)
    if news_item:
        return news_item
    else:
        raise HTTPException(status_code=404, detail="News item not found")


@router.get("/health", tags=["health"])
def health():
    """Health check endpoint."""
    return {"status": "OK"}
