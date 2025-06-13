from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from linkedin_content_creator.types import Rank


@CrewBase
class NewsRanker:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def ranker(self) -> Agent:
        return Agent(
            config=self.agents_config['ranker'],
            verbose=True
        )

    @task
    def rank(self) -> Task:
        return Task(
            config=self.tasks_config['rank'],
            output_pydantic=Rank
        )

    @crew
    def crew(self) -> Crew:
        """Creates the RankNews crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
        )
