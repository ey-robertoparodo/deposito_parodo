from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

from settings import Settings

def split_documents(docs: List[Document]) -> List[Document]:
    """
    Applica uno splitting robusto ai documenti per ottimizzare il retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Settings.chunk_size,
        chunk_overlap=Settings.chunk_overlap,
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