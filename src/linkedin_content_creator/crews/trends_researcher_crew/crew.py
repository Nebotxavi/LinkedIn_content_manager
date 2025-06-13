from pydantic import BaseModel, Field

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from linkedin_content_creator.tools.reddit_trends_searcher_base_tool import RedditTrendsPosts, RedditTrendsSearcher


class Keywords(BaseModel):
    keywords: str = Field(
        ..., description="List of keywords to search for. Example: 'artificial+intelligence+china'")


@CrewBase
class TrendsResearcher:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def keyword_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['keyword_generator'],
            verbose=True
        )

    # @agent
    # def data_getter(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['data_getter'],
    #         verbose=True,
    #         tools=[
    #             RedditTrendsSearcher()
    #         ],
    #     )

    @task
    def generate_keywords(self) -> Task:
        return Task(
            config=self.tasks_config['generate_keywords'],
            output_pydantic=Keywords
        )

    # @task
    # def get_reddit_info(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['get_reddit_info'],
    #         output_pydantic=RedditTrendsPosts,
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the TrendsResearcher crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
