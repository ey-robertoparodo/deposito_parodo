from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from tools_custom.tools.custom_tool import SumTool

@CrewBase
class MathCrew():
    """MathCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def math_professor(self) -> Agent:
        return Agent(
            config=self.agents_config['math_professor'], # type: ignore[index]
            verbose=True,
            tools=[SumTool()],
        )

    @task
    def calculator(self) -> Task:
        return Task(
            config=self.tasks_config['calculator'], # type: ignore[index]
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MathCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
