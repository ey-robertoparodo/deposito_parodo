from pathlib import Path
from typing import List
import faiss
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from settings import Settings
import os


class VectoreStore:

    def __init__(self, persist_dir, embeddings, chunks: List[Document]):
        self.persist_dir = persist_dir
        self.embeddings = embeddings
        self.chunks = chunks
        self.vector_store = self.load_or_build_vectorstore()


    def build_faiss_vectorstore(self) -> FAISS:
        """
        Costruisce da zero un FAISS index (IndexFlatL2) e lo salva su disco.
        """
        # Determina la dimensione dell'embedding
        vs = FAISS.from_documents(documents=self.chunks, embedding=self.embeddings)

        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
        vs.save_local(self.persist_dir)
        return vs


    def load_or_build_vectorstore(self) -> FAISS:
        """
        Tenta il load di un indice FAISS persistente; se non esiste, lo costruisce e lo salva.
        """
        faiss_index_path = os.path.join(Settings.persist_dir, "index.faiss")
        if os.path.exists(faiss_index_path):
            print(f"Carico indice FAISS esistente da {Settings.persist_dir}")
            return FAISS.load_local(
                Settings.persist_dir, self.embeddings, allow_dangerous_deserialization=True
            )
        
        return self.build_faiss_vectorstore(self.chunks, self.embeddings, Settings.persist_dir)
        

    def make_retriever(self):
        """
        Configura il retriever. Con 'mmr' otteniamo risultati meno ridondanti e più coprenti.
        """
        if Settings.search_type == "mmr":
            return self.vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": Settings.k,
                    "fetch_k": Settings.fetch_k,
                    "lambda_mult": Settings.mmr_lambda,
                },
            )
        else:
            return self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": Settings.k},
            )