import os
from typing import List
from PyPDF2 import PdfReader
from langchain.schema import Document

from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import Settings


class DocumentLoader:

    def __init__(self, directory: str):
        self.directory = directory
        self.load_pdfs_from_folder()

    def load_pdfs_from_folder(self) -> List[Document]:
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