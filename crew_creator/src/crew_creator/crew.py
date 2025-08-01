# src/<your_project_name>/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class CrewCreator():
    """CrewCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],  # type: ignore[index]
            verbose=True
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'],  # type: ignore[index]
        )

    @agent
    def file_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['file_creator'],  # type: ignore[index]
            verbose=True
        )

    @task
    def write_files_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_files_task'],  # type: ignore[index]
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the CrewCreator crew"""
        return Crew(
            agents=self.agents,           # Automatically created by the @agent decorator
            tasks=self.tasks,             # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
