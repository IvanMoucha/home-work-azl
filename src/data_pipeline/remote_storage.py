import os

import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem
from src.utils import config

log = logger.get_logger(__name__)


def store(news_item: NewsItem) -> None:
    """
    Sore a news item to remote storage.
    :param news_item:
    :return:
    """

    # Validation logic goes here
    log.debug(f"Storing new news item: {news_item.guid}")

    try:
        file_name = f"{news_item.guid}.json"
        if config.REMOTE_LOCATION.startswith("file://"):
            directory = config.REMOTE_LOCATION[6:]  # Remove 'file://'
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'w') as file:
                file.write(news_item.json())
    except Exception as e:
        log.error(f"Failed to store news item: {news_item.guid} with %s", e)
        raise e
