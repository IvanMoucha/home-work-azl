class NewsItem:
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

