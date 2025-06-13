from linkedin_content_creator.config.general import settings
from linkedin_content_creator.news_provider.google_provider import GoogleNewsProvider
from linkedin_content_creator.news_provider.news_provider import NewsProvider

# Example usage


async def main():
    google_news = GoogleNewsProvider()

    news_provider = NewsProvider(providers=[google_news])

    query = settings.query
    news_items = await news_provider.get_news(query)

    for item in news_items:
        print(f"Title: {item.title}")
        print(f"Source: {item.source}")
        print(f"Date: {item.date}")
        print(f"Link: {item.link}")

        print("---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
