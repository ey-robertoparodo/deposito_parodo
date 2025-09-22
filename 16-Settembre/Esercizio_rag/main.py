from document import DocumentLoader
from vectore_store import VectoreStore
from rag import RagSystem
from models import get_embeddings

from ragas_prova import get_contexts_for_question, build_ragas_dataset, execute_ragas

if __name__ == "__main__":

    doc = DocumentLoader("16-Settembre/Esercizio_rag/docs")

    chunks = doc.split_documents()

    print("Creo db")
    vector_store = VectoreStore("faiss_index_example", get_embeddings(), chunks)

    print("Creo retriever")
    retriever = vector_store.make_retriever()

    print("Creo catena")
    rag = RagSystem(retriever, chunks)

    questions = [
        "Come si può prendere la lode",
        "Qual è la capitale della Francia",
        "Mi spieghi un attimo quali sono i requisti di accesso del corso di laurea Data Science",
        "La capitale della Francia è Berlino",
    ]
    
    ground_truth = {
        questions[0]: "Il voto di laurea si ottiene dalla media ponderata degli esami convertita in centodecimi, a cui si sommano eventuali punti per la rapidità del percorso (fino a +3) e il punteggio per la prova finale (fino a +8, in base alla media). La lode può essere attribuita solo se il voto finale raggiunge almeno 110 e la commissione la approva all’unanimità, rappresentando il massimo riconoscimento del merito accademico e dell’eccellenza del percorso di studi.",
        questions[1]: "La capitale della Francia è Parigi",
        questions[2]: "Per accedere al corso di laurea magistrale in Data Science, Business Analytics e Innovazione (DSBAI) è necessario possedere un numero minimo di crediti in ambiti specifici (24 in discipline economico-aziendali, 15 in matematico-statistici e 11 in informatici), dimostrare la conoscenza della lingua inglese a livello B2 tramite certificazioni riconosciute o esami universitari, e superare una verifica della preparazione personale attraverso una prova scritta che copre matematica generale, statistica, economia aziendale, marketing e informatica. Questo insieme di requisiti garantisce che lo studente disponga delle competenze di base indispensabili per affrontare con successo il percorso magistrale.",
        questions[3]: "No, la capitale della Francia non è Berlino, ma Parigi",
    }

    print("recupero dataset")
    dataset = build_ragas_dataset(questions, retriever, rag, 5, ground_truth)

    print("inizio valutazione ")
    execute_ragas(retriever, rag, dataset)
    
    """
    for q in questions:
        print("=" * 80)
        print("Q:", q)
        print("-" * 80)
        ans = rag.rag_answer(q)
        print(ans)
        print()
    """