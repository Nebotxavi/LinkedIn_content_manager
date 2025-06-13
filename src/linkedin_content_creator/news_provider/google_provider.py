from typing import List

import httpx

from linkedin_content_creator.news_provider.API.google_news.adapter import adapt_to_news_items
from linkedin_content_creator.news_provider.API.google_news.types import NewsAPIResponse, TestAPIResponse
from linkedin_content_creator.config.general import settings
from linkedin_content_creator.types import NewsItem


class GoogleNewsProvider:
    def __init__(self):
        self.api_key = settings.GOOGLE_NEWS_API_KEY
        self.base_url = settings.GOOGLE_NEWS_URL

    async def retrieve_news(self, query: str) -> List[NewsItem]:
        """
        Retrieve news from Google News via SerpAPI
        """
        async with httpx.AsyncClient() as client:
            params = {
                "engine": "google_news",
                "q": query,
                "api_key": self.api_key
            }

            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            data = NewsAPIResponse.model_validate(data)
            news_items = adapt_to_news_items(data)

            return news_items
