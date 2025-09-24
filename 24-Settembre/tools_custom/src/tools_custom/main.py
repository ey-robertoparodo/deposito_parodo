#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from tools_custom.crews.math_crew.math_crew import MathCrew


class ProblemState(BaseModel):
    problems: str = ""
    result: int = 0


class PoemFlow(Flow[ProblemState]):

    @start()
    def generate_sentence_count(self):
        self.state.problems = input("Che somma vuoi fare? ")
        

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = (
            MathCrew()
            .crew()
            .kickoff(inputs={"problem": self.state.problems})
        )

        print("Poem generated", result.raw)
        print(self.state.result)
        self.state.result = int(result.raw)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
