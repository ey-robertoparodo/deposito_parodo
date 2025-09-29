#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from guide_creator_flow.crews.poem_crew.poem_crew import PoemCrew
from guide_creator_flow.crews.rag_crew.rag_crew import RagCrew
from guide_creator_flow.crews.output_crew.output_crew import OutputCrew


class CustomState(BaseModel):
    """Shared state for the flow orchestration.

    Attributes
    ----------
    topic : str
        The general domain or subject that constrains user queries.
    user_query : str
        The last question entered by the user.
    relevance : bool
        Whether the user's question is considered relevant to the topic.
    documents : list
        Retrieved documents related to the user's query.
    """
    topic: str = "Holidays/Trips/Travel/Tourism"
    user_query: str = ""
    relevance: bool = False
    documents: list = []


class PoemFlow(Flow[CustomState]):

    @start()
    def simple_start(self):
        """Entry point for the flow.

        Prints a start message and triggers the next step via the flow
        decorators. This method does not take inputs or return outputs.
        """
        print("Start")

    @listen(or_(simple_start, "Not Relevant"))
    def get_user_query(self):
        """Prompt the user to provide a question within the selected topic.

        The user's input is stored in the shared state under ``user_query``.
        """
        self.state.user_query = input(f"Inserisci la tua domanda rilevante al contesto {self.state.topic}: ")

    @listen(get_user_query)
    def relevance_evaluation(self):
        """Evaluate whether the user's question is relevant to the topic.

        Invokes the `PoemCrew` to assess relevance and updates the shared
        state. The crew returns a mapping that includes a ``relevance`` flag.
        """
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
        """Route the flow depending on the relevance outcome.

        Returns
        -------
        str
            The next step label: ``"Relevant"`` or ``"Not Relevant"``.
        """
        if self.state.relevance:
            return "Relevant"
        print("Domanda non rilevante")
        return "Not Relevant"
    
    @listen("Relevant")
    def vector_search(self):
        """Retrieve relevant documents for the user query.

        Runs the `RagCrew` to perform retrieval and stores the resulting
        documents in the shared state.
        """
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
        """Generate a markdown report based on retrieved documents.

        Executes the `OutputCrew` which first crafts an answer and then
        writes a markdown report to disk.
        """
        print("generate_output")
        result = (
            OutputCrew()
            .crew()
            .kickoff(inputs={"user_query": self.state.user_query,
                             "documents": self.state.documents,
                             "topic":self.state.topic})
        )
        print("Output generato con successo")
    """
    @listen(generate_output)
    def ragas(self):
        #Evaluate the generated answer using RAGAS metrics.

        #Reads the produced ``report.md`` file and runs the evaluation
        #using the project's configured LLM and embeddings.
        
        with open(r"C:\WorkingDirectory\deposito_parodo\24-Settembre\guide_creator_flow\output\report.md", "r", encoding="utf-8") as f:
            read_md = f.read()
            print("Contenuto del file report.md:", read_md[:5])  # Stampa i primi 500 caratteri per verifica
        execute_ragas(self.state.user_query, self.state.documents, read_md)
    """


def kickoff():
    """Run the full flow from start to finish."""
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    """Render the flow graph for visualization or debugging."""
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
