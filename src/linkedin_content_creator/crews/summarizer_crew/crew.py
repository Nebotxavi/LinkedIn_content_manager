from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from linkedin_content_creator.types import Summary


@CrewBase
class NewsSummarizer:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],
            verbose=True
        )

    @task
    def summarize(self) -> Task:
        return Task(
            config=self.tasks_config['summarize'],
            output_pydantic=Summary
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ContentNews crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
