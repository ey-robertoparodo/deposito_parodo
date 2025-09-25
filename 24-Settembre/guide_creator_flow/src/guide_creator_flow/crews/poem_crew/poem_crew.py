from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel

class RelevanceOutput(BaseModel):
    relevance: bool = False

@CrewBase
class PoemCrew:
    """Poem Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def relevance_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["relevance_evaluator"],  # type: ignore[index]
        )

    @task
    def evaluate_relevance(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_relevance"],  # type: ignore[index]
            output_json=RelevanceOutput
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
