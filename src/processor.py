import src.data_pipeline.ingestion as ingestion
import src.utils.config as config
import src.utils.logger as logger


log = logger.get_logger('src.processor')

xml_content = ingestion.fetch_rss_feed(config.DATA_SOURCE)
news_items = ingestion.parse_rss_feed(xml_content)

# for item in news_items:
#     log.debug(item)
