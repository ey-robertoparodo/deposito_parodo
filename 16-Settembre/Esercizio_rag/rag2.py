from load_document import DocumentLoader

from vectore_store import VectoreStore

from splitting_document import split_documents

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate

from models import get_llm_from_lmstudio, get_embeddings


class RagSystem:

    def __init__(self, documents_path: str, db_path: str):
        # 16-Settembre/Esercizio_rag/docs
        self.documents_path = documents_path
        self.db_path = db_path
        doc = DocumentLoader(self.documents_path)
        self.docs = split_documents(doc.load_pdfs_from_folder())

        self.vs = VectoreStore(self.db_path)
        self.retriever = self.vs.make_retriever()

    def format_docs_for_prompt(self) -> str:
        """
        Prepara il contesto per il prompt, includendo citazioni [source].
        """
        lines = []
        for i, d in enumerate(self.docs, start=1):
            src = d.metadata.get("source", f"doc{i}")
            lines.append(f"[source:{src}] {d.page_content}")
        return "\n\n".join(lines)

    def build_rag_chain(self):
        """
        Costruisce la catena RAG (retrieval -> prompt -> LLM) con citazioni e regole anti-hallucination.
        """
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
        chain = (
            {
                "context": self.retriever | self.format_docs_for_prompt,
                "question": RunnablePassthrough(),
            }
            | prompt
            | get_llm_from_lmstudio
            | StrOutputParser()
        )
        return chain

