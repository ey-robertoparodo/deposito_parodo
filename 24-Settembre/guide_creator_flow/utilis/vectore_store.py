from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
import os

class Settings:
    persist_dir: str = "faiss_index_example"
    chunk_size: int = 2000
    chunk_overlap: int = 400
    search_type: str = "mmr" 
    k: int = 4 
    fetch_k: int = 20
    mmr_lambda: float = 0.3

class VectoreStore:

    def __init__(self, persist_dir, embeddings, chunks: List[Document]):
        self.persist_dir = persist_dir
        self.embeddings = embeddings
        self.chunks = chunks

        faiss_index_path = os.path.join(Settings.persist_dir, "index.faiss")
        if os.path.exists(faiss_index_path):
            self.__load_vectorstore()
        else:
            self.__build_faiss_vectorstore()


    def __build_faiss_vectorstore(self) -> FAISS:
        self.vector_store = FAISS.from_documents(documents=self.chunks, embedding=self.embeddings)
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(self.persist_dir)


    def __load_vectorstore(self) -> FAISS:
        self.vector_store = FAISS.load_local(
            Settings.persist_dir, self.embeddings, allow_dangerous_deserialization=True
        )

    def make_retriever(self):
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