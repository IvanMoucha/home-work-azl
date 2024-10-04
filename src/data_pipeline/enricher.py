import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem

log = logger.get_logger(__name__)


def enrich(news_item: NewsItem) -> NewsItem:
    """
    Enrich a news item before storing.
    :param news_item:
    :return:
    """

    # Validation logic goes here
    log.debug(f"Enrich news item: {news_item.guid}")

    return news_item
