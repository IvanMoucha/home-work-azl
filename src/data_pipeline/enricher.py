import requests
from bs4 import BeautifulSoup

import src.utils.logger as logger
from src.data_pipeline.c_newsitem import NewsItem
from src.utils import config

log = logger.get_logger(__name__)

def enrich(news_item: NewsItem) -> NewsItem:
    """
    Enrich a news item before storing.
    :param news_item:
    :return:
    """

    log.debug(f"Enrich news item: {news_item.guid}")

    response = requests.get(news_item.link, headers=config.HEADERS)
    if response.status_code != 200:
        log.warning(f"Failed to retrieve the article. Status code: {response.status_code}")
        return news_item

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article content
    article_body = soup.find('div', {'class': 'article-main'})
    if article_body:
        paragraphs = article_body.find_all('p')
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
    else:
        log.warning(f"Failed to extract the article content: {news_item.link}")
        content = None

    news_item.tldr = content

    return news_item
