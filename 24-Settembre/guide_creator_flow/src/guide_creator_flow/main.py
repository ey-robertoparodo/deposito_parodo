#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from guide_creator_flow.crews.poem_crew.poem_crew import PoemCrew
from guide_creator_flow.crews.rag_crew.rag_crew import RagCrew
from guide_creator_flow.crews.output_crew.output_crew import OutputCrew

from utilis.ragas_prova import execute_ragas



class CustomState(BaseModel):
    topic: str = "Regolamenti universitari o fondi pensione/ viaggi in Francia"
    user_query: str = ""
    relevance: bool = False
    documents: list = []


class PoemFlow(Flow[CustomState]):

    @start()
    def simple_start(self):
        print("Start")

    @listen(or_(simple_start, "Not Relevant"))
    def get_user_query(self):
        self.state.user_query = input(f"Inserisci la tua domanda rilevante al contesto {self.state.topic}: ")

    @listen(get_user_query)
    def relevance_evaluation(self):
        print("relevance_evaluation")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.user_query,
                             "topic":self.state.topic})
        )

        print("Risultato del controllo sulla rilevanza", result)

        if isinstance(result["relevance"], str):
            self.state.relevance = bool(result["relevance"])
        else:
            self.state.relevance = result["relevance"]


    @router(relevance_evaluation)
    def save_poem(self):
        if self.state.relevance:
            return "Relevant"
        print("Domanda non rilevante")
        return "Not Relevant"
    
    @listen("Relevant")
    def vector_search(self):
        print("vector_search")
        result = (
            RagCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.user_query})
        )
        self.state.documents = result["docs"]
        print("Documenti trovati:", self.state.documents)

    @listen(vector_search)
    def generate_output(self):
        print("generate_output")
        result = (
            OutputCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.user_query,
                             "documents": self.state.documents,
                             "topic":self.state.topic})
        )
        print("Output generato con successo")

    @listen(generate_output)
    def ragas(self):
        with open(r"C:\WorkingDirectory\deposito_parodo\24-Settembre\guide_creator_flow\output\report.md", "r", encoding="utf-8") as f:
            read_md = f.read()
            print("Contenuto del file report.md:", read_md[:5])  # Stampa i primi 500 caratteri per verifica
        execute_ragas(self.state.user_query, self.state.documents, read_md)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":    
    kickoff()
