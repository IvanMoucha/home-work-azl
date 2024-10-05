from json import JSONEncoder
from datetime import datetime
from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    description: str
    link: str
    category: str
    pub_date: datetime
    guid: str
    media_thumbnail_url: str
    tldr: str|None = None

    def __init__(self, title, description, link, category, pub_date, guid, media_thumbnail_url):
        self.title = title
        self.description = description
        self.link = link
        self.category = category
        self.pub_date = pub_date
        self.guid = guid
        self.media_thumbnail_url = media_thumbnail_url
        self.tldr = None

    def __repr__(self):
        return f"NewsItem(title={self.title}, pub_date={self.pub_date})"

    def json(self):
        def default(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        return JSONEncoder(default=default).encode(self.__dict__)