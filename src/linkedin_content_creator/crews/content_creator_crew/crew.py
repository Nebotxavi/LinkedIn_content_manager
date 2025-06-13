from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from linkedin_content_creator.types import LinkedInPost


@CrewBase
class ContentCreator:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def post_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['post_creator'],
            verbose=True
        )

    @task
    def create_post(self) -> Task:
        return Task(
            config=self.tasks_config['create_post'],
            output_pydantic=LinkedInPost
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ContentNews crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
        )
