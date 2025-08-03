#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew_creator.crew import CrewCreator
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

prompt = '''
    Im Thinking of a syetem. It takes user's hobbies and suggests careers.
    '''

syntax = '''

    src/project_name/main.py:
    #!/usr/bin/env python
    import sys
    import warnings

    from datetime import datetime

    from project_name.crew import CrewCreator

    warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

    def run():
        """
        Run the crew.
        """
        inputs = {
            'goal': "gOAL of the crew",
            'current_year': str(datetime.now().year)
        }
        
        try:
            CrewCreator().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

    src/project_name/crew.py:
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

        @crew
        def crew(self) -> Crew:
            """Creates the CrewCreator crew"""
            return Crew(
                agents=self.agents,           # Automatically created by the @agent decorator
                tasks=self.tasks,             # Automatically created by the @task decorator
                process=Process.sequential,
                verbose=True,
            )

    src/project_name/__init__.py:
    #keep empty

    src/project_name/config/agents.yaml:
    planner:
    role: >
        Goal Planner Agent
    goal: >
        Given a high-level objective `{goal}`, decompose it into:
        1. A list of agents required (names & brief roles)
        2. A list of tasks each agent must perform
    backstory: >
        You are an expert AI architect who transforms a single sentence of user intent
        into a clear, actionable project plan: agents and tasks required for CREWAI projects

    src/project_name/config/tasks.yaml:
    planning_task:
    description: >
        Take the user's input `{goal}` and produce:
        - An array `agents` of agent names & roles
        - An array `tasks` mapping each agent to their responsibilities
    expected_output: >
        A YAML object with top-level keys `agents`, `tasks`, and `structure`, for example:
        agents:
        - name: planner
            role: Goal Planner Agent
        - name: writer
            role: File Writer Agent
        - name: packager
            role: Packager Agent

        tasks:
        - agent: planner
            task: planning_task
        - agent: writer
            task: writing_task
        - agent: packager
            task: packaging_task
    agent: planner
  '''

def run():
    """
    Run the crew.
    """
    inputs = {
        'goal': prompt,
        'syntax': syntax,
        'base_dir': "./",  # Default base directory for file creation
        'project_name': "MY-lovely-PROJECT",
        'current_year': str(datetime.now().year)
    }
    
    try:
        CrewCreator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

