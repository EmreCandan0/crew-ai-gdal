from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from tools import AnalyzerTool,CropperTool


@CrewBase
class CrewTiffcropper():
    """CrewTiffcropper crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['analyzer'], # type: ignore[index]
            verbose=True,
            tools=[AnalyzerTool()],

        )

    @agent
    def cropper(self) -> Agent:
        return Agent(
            config=self.agents_config['cropper'], # type: ignore[index]
            verbose=True,
            tools=[CropperTool()],

        )


    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_task'], # type: ignore[index]
        )

    @task
    def crop_task(self) -> Task:
        return Task(
            config=self.tasks_config['crop_task'], # type: ignore[index]

        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewTiffcropper crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

        )
