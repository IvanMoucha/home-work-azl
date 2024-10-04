import requests
import xml.etree.ElementTree as ET
from dateutil import parser
import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem
from src.utils import config

log = logger.get_logger(__name__)

def fetch_rss_feed(url):
    try:
        response = requests.get(url, headers=config.HEADERS)
        response.raise_for_status()
        log.info("Successfully fetched RSS feed.")
        return response.content
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching RSS feed: {e}")
        raise

def parse_rss_feed(xml_content):
    root = ET.fromstring(xml_content)
    items = []
    for item in root.findall('./channel/item'):
        news_item = parse_item(item)
        items.append(news_item)
    return items

def parse_item(item):
    media_thumbnail_elem = item.find('media:thumbnail', {'media': 'http://search.yahoo.com/mrss/'})

    return NewsItem(
        title=item.find('title').text,
        description=item.find('description').text,
        link=item.find('link').text,
        category=item.find('category').text.strip() if item.find('category') is not None else None,
        pub_date=parser.parse(item.find('pubDate').text),
        guid=item.find('guid').text,
        media_thumbnail_url=media_thumbnail_elem.attrib['url'] if media_thumbnail_elem is not None else None
    )
