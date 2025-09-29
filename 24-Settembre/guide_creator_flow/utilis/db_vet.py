from typing import List
from dotenv import load_dotenv
from pathlib import Path
from typing import List
import os

#import document, models, vectore_store from utilis
from utilis.document import DocumentLoader
from utilis.vectore_store import VectoreStore
from utilis.models import get_embeddings


load_dotenv()

def initialize_vectorstore():
    """Initialize and return a retriever over a FAISS vector store.

    This function loads PDFs from the project `docs` folder, splits them into
    chunks, builds (or loads) a FAISS index persisted under
    ``faiss_index_example``, and returns a retriever configured according to
    the defaults in `utilis.vectore_store.Settings` (e.g., MMR search).

    Returns
    -------
    Any
        A retriever instance obtained via ``VectoreStore.make_retriever()``
        that can be used to fetch relevant chunks for a query.

    Examples
    --------
    >>> from utilis.db_vet import initialize_vectorstore
    >>> retriever = initialize_vectorstore()  # doctest: +SKIP
    >>> retriever.get_relevant_documents("What is the policy?")  # doctest: +SKIP
    """
    doc = DocumentLoader(r"C:\WorkingDirectory\deposito_parodo\24-Settembre\guide_creator_flow\docs")
    chunks = doc.split_documents()
    vector_store = VectoreStore("faiss_index_example", get_embeddings(), chunks)
    retriever = vector_store.make_retriever()
    return retriever