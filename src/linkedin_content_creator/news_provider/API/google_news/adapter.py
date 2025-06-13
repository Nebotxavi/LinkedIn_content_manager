from datetime import datetime
from typing import List

from linkedin_content_creator.news_provider.API.google_news.types import NewsAPIResponse
from linkedin_content_creator.types import NewsItem


def adapt_to_news_items(api_response: NewsAPIResponse) -> List[NewsItem]:
    return [NewsItem(
        title=entry.title,
        link=entry.link,
        source=entry.source.name,
        date=datetime.strptime(entry.date, "%m/%d/%Y, %I:%M %p, %z UTC"),
        description=None,
        html=None
    ) for entry in api_response.news_results]
