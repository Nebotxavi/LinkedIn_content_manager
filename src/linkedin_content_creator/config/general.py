from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_NEWS_API_KEY: str
    OPENAI_API_KEY: str
    MODEL: str = "gpt-4o-mini"
    GOOGLE_NEWS_URL: str = "https://serpapi.com/search.json"

    scrap_news_limit: int = 10
    summary_news_limit: int = 10

    topic: str = "Artificial Intelligence in China"
    user_interests: str = """
        Artificial Intelligence, LLMs, AI startups and agentic systems;
        all related to China or happening in China
        """
    priority_1: str = "Agentic systems related"
    priority_2: str = "Large Language Models (LLM)"
    priority_3: str = "Artificial Intelligence in China"
    priority_4: str = "Startups, ecosystem and government decisions related to AI in China"
    additional_criteria: str = """
    - News that focus on the artificial intelligence ecosystem in China
      and provide valuable insights about this not very well known topic in western media
    - Articles that avoid the hype and provide a deep understanding of the technology
        or the impact of the disruptive technology. Example: avoid pessimistic news
        about AI controlling the world, give points to news that understand how a new algorithm
        that makes models to learn faster means a lot for the industry
    """
    remark: str = "All news must be related to China and Artificial Intelligence"
    query: str = "artificial+intelligence+AND+China+when:1d"

    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()
