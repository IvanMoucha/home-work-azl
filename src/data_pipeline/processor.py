import src.utils.logger as logger
import src.database.dao_news as dao_news
from src.data_pipeline.c_newsitem import NewsItem
from src.data_pipeline.corruption_handler import handle_corrupt_data, handle_errors
from src.data_pipeline.enricher import enrich
from src.data_pipeline.remote_storage import store
from src.data_pipeline.validator import validate

log = logger.get_logger(__name__)

def process_news_item(news_item: NewsItem):
    log.debug(f"Processing news item: {news_item.title}")

    try:
        process = False
        if validate(news_item):
            process = True
        else:
            if handle_corrupt_data(news_item) is not None:
                process = True

        news_item = enrich(news_item)

        if process and dao_news.guid_exists(news_item.guid):
            dao_news.update_news_item(news_item)
            log.debug(f"Updated news item: {news_item.guid}")
        elif process:
            dao_news.insert_news_item(news_item)
            store(news_item)
            log.debug(f"Inserted news item: {news_item.guid}")
    except Exception as e:
        handle_errors(news_item, e)
