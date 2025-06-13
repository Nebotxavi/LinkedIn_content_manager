from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from linkedin_content_creator.types import TrendAnalysis


@CrewBase
class TrendsAnalyst:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trends_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['trends_analyst'],
            verbose=True
        )

    @task
    def analyze_trends(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_trends'],
            output_pydantic=TrendAnalysis
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TrendsAnalyst crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
        )
