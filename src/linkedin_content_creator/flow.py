import copy
from datetime import datetime
from typing import List, TypedDict

from crewai.flow.flow import Flow, start, listen, and_

from linkedin_content_creator.adapters import adapt_news_item_for_crew
from linkedin_content_creator.config.general import settings
from linkedin_content_creator.crews.content_creator_crew.crew import ContentCreator
from linkedin_content_creator.crews.summarizer_crew.crew import NewsSummarizer
from linkedin_content_creator.crews.rank_crew.crew import NewsRanker
from linkedin_content_creator.crews.trends_analist_crew.crew import TrendsAnalyst
from linkedin_content_creator.crews.trends_researcher_crew.crew import Keywords, TrendsResearcher
from linkedin_content_creator.news_provider.google_provider import GoogleNewsProvider
from linkedin_content_creator.news_provider.news_provider import NewsProvider
from linkedin_content_creator.report_provider.report_provider import NewsReportGenerator
from linkedin_content_creator.tools.reddit_trends_searcher import fetch_reddit_data
from linkedin_content_creator.types import FetchErrorItem, LinkedInPost, NewsItem, Rank, Summary, TrendAnalysis


class LinkedinFlowState(TypedDict):
    news_items: List[NewsItem]
    fetch_error_items: List[FetchErrorItem]


class LinkedinContentCreationFlow(Flow):
    state: LinkedinFlowState

    @start()
    async def get_news(self) -> None:
        google_news = GoogleNewsProvider()

        news_provider = NewsProvider(providers=[google_news])

        query = settings.query
        limit = settings.scrap_news_limit
        news_items, fetch_error_items = await news_provider.get_news(query, limit)

        self.state["news_items"] = news_items
        self.state['fetch_error_items'] = fetch_error_items

    @listen(get_news)
    def rank_news(self) -> None:
        print("Start ranking news")

        for news_item in self.state['news_items']:
            news_item_copy = copy.deepcopy(news_item)
            adapted_news_item = adapt_news_item_for_crew(news_item_copy)

            output = NewsRanker().crew().kickoff(adapted_news_item)

            rank: Rank = output.pydantic
            news_item.rank = rank.rank
            news_item.rank_explanation = rank.report

    @listen(rank_news)
    def filter_by_rank(self) -> None:
        print("Start filtering news by ranking")

        news_items: List[NewsItem] = self.state['news_items']

        sorted_news = sorted(news_items, key=lambda x: x.rank, reverse=True)

        limit = settings.summary_news_limit
        limit = len(sorted_news) - 1 if limit == 0 or limit >= len(
            sorted_news) else limit

        # Correct limit in edge case where there is only one article
        if (limit == 0 and len(sorted_news) == 1):
            limit = 1

        limited_news = sorted_news[0:limit]

        self.state['news_items'] = limited_news

    @listen(filter_by_rank)
    def generate_summary(self) -> None:
        print("Start generating summary")

        for news_item in self.state['news_items']:
            news_item_copy = copy.deepcopy(news_item)
            adapted_news_item = adapt_news_item_for_crew(news_item_copy)

            output = NewsSummarizer().crew().kickoff(adapted_news_item)

            summary: Summary = output.pydantic
            news_item.summary = summary.summary

    @listen(generate_summary)
    def generate_keywords(self) -> None:
        print("Start generating keywords")

        for news_item in self.state['news_items']:

            output = TrendsResearcher().crew().kickoff(inputs={
                'article_summary': news_item.summary,
                'user_interests': settings.user_interests
            })

            keywords_entity: Keywords = output.pydantic
            news_item.keywords = keywords_entity.keywords

    @listen(generate_keywords)
    def get_trends(self) -> None:
        print("Start getting trends")

        for news_item in self.state['news_items']:
            reddit_content = fetch_reddit_data(news_item.keywords)
            news_item.reddit_content = reddit_content

    @listen(get_trends)
    def generate_linkedin_post(self) -> None:
        print("Start generating linkedin post")

        for news_item in self.state['news_items']:
            news_item_copy = copy.deepcopy(news_item)
            adapted_news_item = adapt_news_item_for_crew(news_item_copy)

            output = ContentCreator().crew().kickoff(adapted_news_item)

            linkedin_post: LinkedInPost = output.pydantic
            news_item.linkedin_post = linkedin_post.post

    @listen(get_trends)
    def generate_trends_summary(self) -> None:
        print("Start generating trends summary")

        for news_item in self.state['news_items']:
            news_item_copy = copy.deepcopy(news_item)
            reddit_messages_list = [
                reddit_item.to_prompt_format() for reddit_item in news_item_copy.reddit_content]

            reddit_messages = ' \n '.join(reddit_messages_list)

            output = TrendsAnalyst().crew().kickoff(inputs={
                'social_media_content': reddit_messages,
                'user_interests': settings.user_interests,
                'text': news_item_copy.summary,
                'title': news_item_copy.title,
                'topic': settings.topic,
                'priority_1': settings.priority_1,
                'priority_2': settings.priority_2,
                'priority_3': settings.priority_3,
                'priority_4': settings.priority_4,
            })

            trends_analysis: TrendAnalysis = output.pydantic
            news_item.trends_analysis = trends_analysis

    @listen(and_(generate_summary, generate_linkedin_post))
    def show_results(self) -> None:
        generator = NewsReportGenerator(self.state['news_items'])
        html_report = generator.generate_html_report()
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Write to a file or serve it
        with open(f"news_report_{now}.html", "w", encoding="utf-8") as f:
            f.write(html_report)


flow = LinkedinContentCreationFlow()
