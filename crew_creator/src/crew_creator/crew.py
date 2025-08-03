from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.crew_creator.tools.file_writer_tool import FileWriteTool
from src.crew_creator.tools.shell_tool import ShellTool
from src.crew_creator.tools.project_init_tool import ProjectInitTool

@CrewBase
class CrewCreator():
    """CrewCreator crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def folder_initializer(self) -> Agent:
        return Agent(
            config=self.agents_config['folder_initializer'], 
            tools=[ShellTool(), ProjectInitTool()],
            verbose=True
        )
        

    @task
    def initialize_folder_task(self) -> Task:
        return Task(
            config=self.tasks_config['initialize_folder_task']
        )


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
            tools=[FileWriteTool()],
            verbose=True
        )

    @task
    def write_files_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_files_task'],  # type: ignore[index]
            context=[
                self.initialize_folder_task(),
                self.planning_task()
            ],
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
