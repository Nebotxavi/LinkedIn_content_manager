from typing import Protocol, List

from bs4 import BeautifulSoup

import httpx

from linkedin_content_creator.types import FetchErrorItem, NewsItem


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


class NewsProviderProtocol(Protocol):
    async def retrieve_news(self, query: str) -> List[NewsItem]:
        ...


class NewsProvider:
    def __init__(self, providers: List[NewsProviderProtocol]):
        self.providers = providers

    async def _fetch_content(self, news_items: List[NewsItem]) -> List[NewsItem]:

        processed_items: List[NewsItem] = []
        fetch_error_items: List[FetchErrorItem] = []

        async with httpx.AsyncClient() as client:

            for item in news_items:
                try:
                    response = await client.get(str(item.link), headers=headers)
                    response.raise_for_status()

                    item.html = response.text

                    soup = BeautifulSoup(response.text, 'html.parser')
                    item.text = soup.get_text(separator=' ', strip=True)

                    processed_items.append(item)
                except Exception as e:
                    fetch_error_items.append(
                        FetchErrorItem(link=str(item.link), error=str(e), title=item.title))
                    print("Error fetching content: ", e)
                    print('---')

        return (processed_items, fetch_error_items)

    async def get_news(self, query: str, limit: int = 0) -> tuple[List[NewsItem], List[FetchErrorItem]]:
        """
        Retrieve news from all configured providers
        """
        all_news: List[NewsItem] = []
        fetch_error_items: List[FetchErrorItem] = []

        for provider in self.providers:
            try:
                news_items = await provider.retrieve_news(query)
                print(f'News headers retrieved: {len(news_items)}')

                news_items_with_content, fetch_errors = await self._fetch_content(news_items)
                print(f'News with content retrieved: '
                      f'{len(news_items_with_content)}')

                all_news.extend(news_items_with_content)
                fetch_error_items.extend(fetch_errors)
            except Exception as e:
                print(f"Error retrieving news from provider: {e}")

        sorted_news = sorted(all_news, key=lambda x: x.date, reverse=True)
        limit = len(sorted_news) - 1 if limit == 0 or limit >= len(
            sorted_news) else limit

        # Correct limit in edge case where there is only one article
        if (limit == 0 and len(sorted_news) == 1):
            limit = 1

        print(f"Returning {limit} news items")

        return (sorted_news[0:limit], fetch_error_items)
