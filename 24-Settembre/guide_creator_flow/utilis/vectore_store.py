from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
import os

class Settings:
    """Configuration parameters for the FAISS-backed vector store.

    Attributes
    ----------
    persist_dir : str
        Directory where the FAISS index is read/written.
    chunk_size : int
        Unused here (duplicated from document settings), kept for consistency.
    chunk_overlap : int
        Unused here (duplicated from document settings), kept for consistency.
    search_type : str
        Retrieval mode. Supported values are ``"mmr"`` and ``"similarity"``.
    k : int
        Number of results to return from the retriever.
    fetch_k : int
        Candidate pool size used by MMR retrieval.
    mmr_lambda : float
        Diversity vs relevance trade-off for MMR in \[0, 1].
    """
    persist_dir: str = "faiss_index_example"
    chunk_size: int = 2000
    chunk_overlap: int = 400
    search_type: str = "mmr" 
    k: int = 4 
    fetch_k: int = 20
    mmr_lambda: float = 0.3

class VectoreStore:

    def __init__(self, persist_dir, embeddings, chunks: List[Document]):
        """Create or load a FAISS vector store and prepare it for retrieval.

        Parameters
        ----------
        persist_dir : str
            Directory where the FAISS index is stored. Created if missing.
        embeddings : Any
            Embeddings client implementing the LangChain embeddings interface.
        chunks : List[Document]
            Pre-split `Document` items used to build the vector index if one
            does not already exist at ``persist_dir``.

        Notes
        -----
        If a file named ``index.faiss`` exists in ``Settings.persist_dir``,
        that index is loaded; otherwise a new index is built from ``chunks``
        and saved to disk.
        """
        self.persist_dir = persist_dir
        self.embeddings = embeddings
        self.chunks = chunks

        faiss_index_path = os.path.join(Settings.persist_dir, "index.faiss")
        if os.path.exists(faiss_index_path):
            self.__load_vectorstore()
        else:
            self.__build_faiss_vectorstore()


    def __build_faiss_vectorstore(self) -> FAISS:
        """Build a new FAISS index from the provided chunks and persist it.

        Returns
        -------
        FAISS
            The created FAISS vector store instance.
        """
        self.vector_store = FAISS.from_documents(documents=self.chunks, embedding=self.embeddings)
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(self.persist_dir)


    def __load_vectorstore(self) -> FAISS:
        """Load an existing FAISS index from disk.

        Returns
        -------
        FAISS
            The loaded FAISS vector store instance.
        """
        self.vector_store = FAISS.load_local(
            Settings.persist_dir, self.embeddings, allow_dangerous_deserialization=True
        )

    def make_retriever(self):
        """Create a retriever configured with the selected search strategy.

        Returns
        -------
        Any
            A retriever object exposing ``get_relevant_documents(query)``.

        Notes
        -----
        When ``Settings.search_type == 'mmr'``, returns an MMR-based retriever
        tuned by ``k``, ``fetch_k``, and ``mmr_lambda``; otherwise returns a
        standard similarity retriever with ``k`` top results.
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