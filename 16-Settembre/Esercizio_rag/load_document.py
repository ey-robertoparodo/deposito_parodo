import os
from typing import List
from PyPDF2 import PdfReader
from langchain.schema import Document


class DocumentLoader:

    def __init__(self, directory: str):
        self.directory = directory


    def load_pdfs_from_folder(self) -> List[Document]:
        pdf_documents = []
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.directory, filename)
                try:
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    pdf_documents.append(Document(page_content=text, metadata={"source": filename}))
                except Exception as e:
                    print(f"Errore nella lettura di {filename}: {e}")
        return pdf_documents
    

if __name__ == "__main__":
    doc = DocumentLoader("16-Settembre/Esercizio_rag/docs")
    print("start")
    print(doc.load_pdfs_from_folder())
