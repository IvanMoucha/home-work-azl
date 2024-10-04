import src.data_pipeline.ingestion as ingestion
import src.utils.config as config
import src.utils.logger as logger
import src.database.db as db
import src.database.m_news as news
from src.data_pipeline import processor

log = logger.get_logger('src.processor')

db.init()
news.init()

xml_content = ingestion.fetch_rss_feed(config.DATA_SOURCE)
news_items = ingestion.parse_rss_feed(xml_content)

for item in news_items:
    processor.process_news_item(item)
