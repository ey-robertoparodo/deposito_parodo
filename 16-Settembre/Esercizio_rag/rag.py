from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain.schema import Document
from models import get_llm


class RagSystem:

    def __init__(self, retriever, docs: List[Document]):
        self.retriever = retriever
        self.docs = docs
        self.build_rag_chain()

    def format_docs_for_prompt(self, docs) -> str:
        lines = []
        for i, d in enumerate(docs, start=1):
            src = d.metadata.get("source", f"doc{i}")
            lines.append(f"[source:{src}] {d.page_content}")
        return "\n\n".join(lines)

    def build_rag_chain(self):
        system_prompt = (
            "Sei un assistente esperto. Rispondi in italiano. "
            "Usa esclusivamente il CONTENUTO fornito nel contesto. "
            "Se l'informazione non è presente, dichiara che non è disponibile. "
            "Includi citazioni tra parentesi quadre nel formato [source:...]. "
            "Sii conciso, accurato e tecnicamente corretto."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                (
                    "human",
                    "Domanda:\n{question}\n\n"
                    "Contesto (estratti selezionati):\n{context}\n\n"
                    "Istruzioni:\n"
                    "1) Rispondi solo con informazioni contenute nel contesto.\n"
                    "2) Cita sempre le fonti pertinenti nel formato [source:FILE].\n"
                    "3) Se la risposta non è nel contesto, scrivi: 'Non è presente nel contesto fornito.'",
                ),
            ]
        )

        # LCEL: dict -> prompt -> llm -> parser
        self.chain = (
            {
                "context": self.retriever | self.format_docs_for_prompt,
                "question": RunnablePassthrough(),
            }
            | prompt
            | get_llm()
            | StrOutputParser()
        )
    
    def rag_answer(self, question: str) -> str:
        return self.chain.invoke(question)