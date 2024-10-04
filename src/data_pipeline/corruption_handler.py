import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem

log = logger.get_logger(__name__)


def handle_corrupt_data(news_item: NewsItem) -> NewsItem|None:
    """
    Handle corrupt data in the news item.
    :param news_item:
    :return:
    """

    # Corruption data handling logic
    log.debug(f"Handling corrupt data for news item: {news_item.guid}")

    return news_item

def handle_errors(news_item: NewsItem, e: Exception) -> None:
    """
    Handle corrupt data in the news item.
    :param news_item:
    :return:
    """

    # Corruption data handling logic
    log.debug(f"Handling errors for news item: {news_item.guid} with exception: %s", e)

