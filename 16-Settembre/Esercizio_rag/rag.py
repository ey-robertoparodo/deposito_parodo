from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

import faiss
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LangChain Core (prompt/chain)
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Chat model init (provider-agnostic, qui puntiamo a LM Studio via OpenAI-compatible)
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from load_document import DocumentLoader


# =========================
# Configurazione
# =========================

load_dotenv()


@dataclass
class Settings:
    # Persistenza FAISS
    persist_dir: str = "faiss_index_example"
    # Text splitting
    chunk_size: int = 2000
    chunk_overlap: int = 400
    # Retriever (MMR)
    search_type: str = "mmr"  # "mmr" o "similarity"
    k: int = 4  # risultati finali
    fetch_k: int = 20  # candidati iniziali (per MMR)
    mmr_lambda: float = 0.3  # 0 = diversificazione massima, 1 = pertinenza massima
    # Embedding
    hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    # LM Studio (OpenAI-compatible)
    lmstudio_model_env: str = (
        "LMSTUDIO_MODEL"  # nome del modello in LM Studio, via env var
    )


SETTINGS = Settings()

# =========================
# Componenti di base
# =========================


def get_embeddings(settings: Settings) -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("OPEN_API_KEY"),
        api_version=os.getenv("API_VERSION_EMBED"),
    )


def get_llm_from_lmstudio(settings: Settings):
    return AzureChatOpenAI(
        deployment_name="gpt-4o",
        api_version=os.getenv("API_VERSION"),
        azure_endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("OPEN_API_KEY"),
    )


def split_documents(docs: List[Document], settings: Settings) -> List[Document]:
    """
    Applica uno splitting robusto ai documenti per ottimizzare il retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            "; ",
            ": ",
            ", ",
            " ",
            "",  # fallback aggressivo
        ],
    )
    return splitter.split_documents(docs)


def build_faiss_vectorstore(
    chunks: List[Document], embeddings: HuggingFaceEmbeddings, persist_dir: str
) -> FAISS:
    """
    Costruisce da zero un FAISS index (IndexFlatL2) e lo salva su disco.
    """
    # Determina la dimensione dell'embedding
    vs = FAISS.from_documents(documents=chunks, embedding=embeddings)

    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    vs.save_local(persist_dir)
    return vs


def load_or_build_vectorstore(
    settings: Settings, embeddings: HuggingFaceEmbeddings, docs: List[Document]
) -> FAISS:
    """
    Tenta il load di un indice FAISS persistente; se non esiste, lo costruisce e lo salva.
    """
    # Se l'indice FAISS esiste già, caricalo, altrimenti crealo
    import os

    faiss_index_path = os.path.join(settings.persist_dir, "index.faiss")
    if os.path.exists(faiss_index_path):
        print(f"Carico indice FAISS esistente da {settings.persist_dir}")
        return FAISS.load_local(
            settings.persist_dir, embeddings, allow_dangerous_deserialization=True
        )
    else:
        print("Creo nuovo indice FAISS...")
        chunks = split_documents(docs, settings)
        return build_faiss_vectorstore(chunks, embeddings, settings.persist_dir)


def make_retriever(vector_store: FAISS, settings: Settings):
    """
    Configura il retriever. Con 'mmr' otteniamo risultati meno ridondanti e più coprenti.
    """
    if settings.search_type == "mmr":
        return vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": settings.k,
                "fetch_k": settings.fetch_k,
                "lambda_mult": settings.mmr_lambda,
            },
        )
    else:
        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": settings.k},
        )


def format_docs_for_prompt(docs: List[Document]) -> str:
    """
    Prepara il contesto per il prompt, includendo citazioni [source].
    """
    lines = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", f"doc{i}")
        lines.append(f"[source:{src}] {d.page_content}")
    return "\n\n".join(lines)


def build_rag_chain(llm, retriever):
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
            "context": retriever | format_docs_for_prompt,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def rag_answer(question: str, chain) -> str:
    """
    Esegue la catena RAG per una singola domanda.
    """
    return chain.invoke(question)


# =========================
# Esecuzione dimostrativa
# =========================


def main():
    settings = SETTINGS

    # 1) Componenti
    embeddings = get_embeddings(settings)
    llm = get_llm_from_lmstudio(settings)

    # 2) Dati simulati e indicizzazione (load or build)
    doc = DocumentLoader("16-Settembre/Esercizio_rag/docs")
    docs = doc.load_pdfs_from_folder()
    vector_store = load_or_build_vectorstore(settings, embeddings, docs)

    # 3) Retriever ottimizzato
    retriever = make_retriever(vector_store, settings)

    # 4) Catena RAG
    chain = build_rag_chain(llm, retriever)

    # 5) Esempi di domande
    questions = [
        "Come si può prendere la lode",
        "Chi è Cristiano Ronaldo",
        "Qual è la captale della Francia",
        "che esami devo aver superato per poter iniziare il tirocinio",
        "La capitale della Francia è Berlino",
    ]

    for q in questions:
        print("=" * 80)
        print("Q:", q)
        print("-" * 80)
        ans = rag_answer(q, chain)
        print(ans)
        print()


if __name__ == "__main__":
    main()
