import os
from typing import List
from PyPDF2 import PdfReader
from langchain.schema import Document

from langchain.text_splitter import RecursiveCharacterTextSplitter

class Settings:
    """Configuration for document processing.

    Attributes
    ----------
    persist_dir : str
        Directory where artifacts (e.g., FAISS index) are persisted.
    chunk_size : int
        Target size of each text chunk when splitting documents.
    chunk_overlap : int
        Number of overlapping characters between consecutive chunks.
    search_type : str
        Default retrieval mode. Supported values are ``"mmr"`` and
        ``"similarity"``.
    k : int
        Number of results to return for retrieval operations.
    fetch_k : int
        Oversampling parameter for MMR retrieval that controls candidate pool.
    mmr_lambda : float
        Trade-off parameter for MMR between diversity and relevance
        in \[0, 1].
    """
    persist_dir: str = "faiss_index_example"
    chunk_size: int = 2000
    chunk_overlap: int = 400
    search_type: str = "mmr" 
    k: int = 4 
    fetch_k: int = 20
    mmr_lambda: float = 0.3


class DocumentLoader:

    def __init__(self, directory: str):
        """Initialize a PDF loader and eagerly parse all PDFs in a folder.

        Parameters
        ----------
        directory : str
            Path to the directory containing PDF files. All ``.pdf`` files
            in this folder will be loaded into memory on initialization.
        """
        self.directory = directory
        self.load_pdfs_from_folder()

    def load_pdfs_from_folder(self) -> List[Document]:
        """Read all PDFs in the configured folder and convert to Documents.

        Returns
        -------
        List[Document]
            A list of LangChain `Document` objects, one per PDF file, where
            the text is the concatenation of all pages and metadata contains
            the source filename under the key ``"source"``.

        Raises
        ------
        Exception
            Any exception raised by `PyPDF2.PdfReader` while parsing a file
            is caught and printed, and the file is skipped. The method itself
            does not re-raise but continues processing remaining files.
        """
        self.pdf_documents = []
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.directory, filename)
                try:
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    self.pdf_documents.append(
                        Document(page_content=text, metadata={"source": filename})
                    )
                except Exception as e:
                    print(f"Errore nella lettura di {filename}: {e}")
        return self.pdf_documents
    
    def split_documents(self) -> List[Document]:
        """Split loaded PDFs into semantically sized text chunks.

        Uses `RecursiveCharacterTextSplitter` with a mix of paragraph, sentence,
        and token-like separators to produce overlapping chunks that work well
        for retrieval scenarios.

        Returns
        -------
        List[Document]
            Chunked `Document` objects derived from the loaded PDFs.

        Notes
        -----
        Chunking behavior is governed by `Settings.chunk_size` and
        `Settings.chunk_overlap`.
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
                "",
            ],
        )
        return splitter.split_documents(self.pdf_documents)