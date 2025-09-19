from document import DocumentLoader
from vectore_store import VectoreStore
from rag import RagSystem
from models import get_embeddings

if __name__ == "__main__":

    doc = DocumentLoader("16-Settembre/Esercizio_rag/docs")

    chunks = doc.split_documents()

    vector_store = VectoreStore("faiss_index_example", get_embeddings(), chunks)

    retriever = vector_store.make_retriever()

    rag = RagSystem(retriever, chunks)

    questions = [
        "Come si può prendere la lode",
        "Chi è Cristiano Ronaldo",
        "Qual è la captale della Francia",
        "Mi spieghi un attimo quali sono i requisti di accesso del corso di laurea Data Science",
        "La capitale della Francia è Berlino",
    ]

    for q in questions:
        print("=" * 80)
        print("Q:", q)
        print("-" * 80)
        ans = rag.rag_answer(q)
        print(ans)
        print()