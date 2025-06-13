from linkedin_content_creator.config.general import settings
from linkedin_content_creator.types import NewsItem, NewsItemForRanking


def adapt_news_item_for_crew(news_item: NewsItem):
    common_attributes = {
        'topic': settings.topic,
        'user_interests': settings.user_interests,
        'priority_1': settings.priority_1,
        'priority_2': settings.priority_2,
        'priority_3': settings.priority_3,
        'priority_4': settings.priority_4,
        "additional_criteria": settings.additional_criteria,
        "remark": settings.remark

    }

    adapted_new_item = NewsItemForRanking(
        title=news_item.title,
        source=news_item.source,
        date=news_item.date,
        link=str(news_item.link),
        text=news_item.text,
        **common_attributes
    )

    return adapted_new_item.model_dump()
