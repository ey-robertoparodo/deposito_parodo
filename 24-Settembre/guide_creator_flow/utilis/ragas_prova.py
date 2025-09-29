"""Utilities to build datasets and run RAGAS evaluation over RAG outputs.

This module provides helpers to synthesize ground-truth answers with an LLM,
assemble RAGAS-compatible datasets, and execute a suite of RAGAS metrics
using the project's configured LLM and embeddings.
"""
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
    """Synthesize a reference answer using the LLM and retrieved contexts.

    Parameters
    ----------
    query : str
        The user question for which a reference answer will be generated.
    documents : List[Any]
        Retrieved contexts. Each document is expected to expose the key
        ``"page_content"`` containing text used to guide the generation.

    Returns
    -------
    str
        A reference answer produced by the LLM, conditioned on the provided
        contexts.

    Examples
    --------
    >>> from utilis.ragas_prova import get_ground_truth_for_query
    >>> docs = [{"page_content": "policy text..."}]
    >>> ref = get_ground_truth_for_query("What is the policy?", docs)  # doctest: +SKIP
    """
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
    """Build a list of rows compatible with RAGAS `EvaluationDataset`.

    Each row includes the user question, the retrieved contexts, the model's
    answer to be evaluated, and a synthesized reference answer.

    Parameters
    ----------
    query : str
        The user input or question being evaluated.
    documents : List[Any]
        Retrieved contexts. Each must include a ``"page_content"`` key.
    answer : str
        The model-generated answer to evaluate against the metrics.

    Returns
    -------
    List[dict]
        A list of dataset rows, suitable for creating a
        ``ragas.EvaluationDataset``.

    Examples
    --------
    >>> from utilis.ragas_prova import build_ragas_dataset
    >>> rows = build_ragas_dataset("Q?", [{"page_content": "ctx"}], "A")  # doctest: +SKIP
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
    """Run RAGAS metrics and persist results to ``ragas_results.csv``.

    Parameters
    ----------
    user_query : str
        The user question that the answer attempts to address.
    documents : List[Any]
        Retrieved contexts used to ground the answer. Each must include
        ``"page_content"``.
    file_md : str
        The answer content (e.g., markdown) produced by your RAG pipeline.

    Returns
    -------
    None
        Results are printed to stdout and written to ``ragas_results.csv``.

    Notes
    -----
    The metrics computed include context precision/recall, faithfulness,
    answer relevancy, and answer correctness (when reference answers are
    available for all rows).

    Examples
    --------
    >>> from utilis.ragas_prova import execute_ragas
    >>> execute_ragas("Q?", [{"page_content": "ctx"}], "A")  # doctest: +SKIP
    """
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