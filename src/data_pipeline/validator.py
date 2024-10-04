import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem

log = logger.get_logger(__name__)


def validate(news_item: NewsItem) -> bool:
    """
    Validate a news item before processing.
    :param news_item:
    :return:
    """

    # Validation logic goes here
    log.debug(f"Validating news item: {news_item.guid}")

    return True
