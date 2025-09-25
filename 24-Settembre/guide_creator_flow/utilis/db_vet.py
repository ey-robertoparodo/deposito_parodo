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
    doc = DocumentLoader(r"C:\WorkingDirectory\deposito_parodo\24-Settembre\guide_creator_flow\docs")
    chunks = doc.split_documents()
    vector_store = VectoreStore("faiss_index_example", get_embeddings(), chunks)
    retriever = vector_store.make_retriever()
    return retriever