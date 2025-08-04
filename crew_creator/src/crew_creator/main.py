#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew_creator.crew import CrewCreator
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

prompt = '''
    Im Thinking of a syetem. It takes ingredients and suggests me recipies. Create a skeleton for this.
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
            'goal': "GOAL of the crew",
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
        def agent_name(self) -> Agent:
            return Agent(
                config=self.agents_config['agent_name'],  # type: ignore[index]
                verbose=True
            )

        @task
        def agent_task(self) -> Task:
            return Task(
                config=self.tasks_config['agent_task'],  # type: ignore[index]
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
    agent_name:
    role: >
        Agent's goal
    goal: >
        Given a ....
    backstory: >
        You are an expert ...

    src/project_name/config/tasks.yaml:
    agent_task:
    description: >
        Take the ...
    expected_output: >
        A ....
    agent: agent_name
  '''

def run(inputs):
    """
    Run the crew.
    """
    # inputs = {
    #     'goal': prompt,
    #     'syntax': syntax,
    #     'base_dir': "./",  # Default base directory for file creation
    #     'project_name': "MY-lovely-PROJECT",
    #     'current_year': str(datetime.now().year)
    # }
    
    try:
        CrewCreator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

