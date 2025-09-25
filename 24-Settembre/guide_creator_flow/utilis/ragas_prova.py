from ragas import evaluate, EvaluationDataset
from ragas.metrics import (
    context_precision,   # "precision@k" sui chunk recuperati
    context_recall,      # copertura dei chunk rilevanti
    faithfulness,        # ancoraggio della risposta al contesto
    answer_relevancy,    # pertinenza della risposta vs domanda
    answer_correctness,  # usa questa solo se hai ground_truth
)
from typing import List, Any
from utilis.models import get_embeddings, get_llm

def get_ground_truth_for_query(query: str, documents: List[Any]) -> str:
    llm = get_llm()

    joined = "\n---\n".join([document["page_content"] for document in documents])

    prompt = f"""Sei un assistente che crea file.md per rispondere alla domanda dell'utente.
            Domanda: {query}

            Contesti:
            {joined}

            Risposta:"""

    response = llm.invoke(prompt)
    response_text = response.content
    return response_text

def build_ragas_dataset(
    query: str,
    documents: List[Any],
    answer: str
):
    """
    Esegue la pipeline RAG per ogni domanda e costruisce il dataset per Ragas.
    Ogni riga contiene: question, contexts, answer, (opzionale) ground_truth.
    """
    dataset = []

    row = {
        # chiavi richieste da molte metriche Ragas
        "user_input": query,
        "retrieved_contexts": [document["page_content"] for document in documents],
        "response": answer,
        "reference": get_ground_truth_for_query(query, documents)
    }


    dataset.append(row)
    return dataset

def execute_ragas(user_query, documents, file_md):
    print("Eseguo RAGAS...")
    dataset = build_ragas_dataset(
        query=user_query,
        documents=documents,
        answer=file_md
    )
    print("Dataset per RAGAS:", dataset)

    evaluation_dataset = EvaluationDataset.from_list(dataset)

    print("Eseguo valutazione RAGAS...")
    metrics = [context_precision, context_recall, faithfulness, answer_relevancy, answer_correctness]
    # Aggiungi correctness solo se tutte le righe hanno ground_truth
    # if all("ground_truth" in row for row in dataset):
    #     metrics.append(answer_correctness)

    # 8) Esegui la valutazione con il TUO LLM e le TUE embeddings
    ragas_result = evaluate(
        dataset=evaluation_dataset,
        metrics=metrics,
        llm=get_llm(),                 # passa l'istanza LangChain del tuo LLM (LM Studio)
        embeddings=get_embeddings(),  # o riusa 'embeddings' creato sopra
    )

    df = ragas_result.to_pandas()
    cols = ["user_input", "response", "context_precision", "context_recall", "faithfulness", "answer_relevancy"]
    print("\n=== DETTAGLIO PER ESEMPIO ===")
    print(df[cols].round(4).to_string(index=False))

    # (facoltativo) salva per revisione umana
    df.to_csv("ragas_results.csv", index=False, sep=";")
    print("Salvato: ragas_results.csv")