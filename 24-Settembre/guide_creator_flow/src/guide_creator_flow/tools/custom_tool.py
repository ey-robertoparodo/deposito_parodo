from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai.tools import tool

from utilis.db_vet import initialize_vectorstore

@tool("RAGSearch")
def RAGSearch(query: str) -> str:
    """Run a similarity search over the vector store.

    Parameters
    ----------
    query : str
        The search query string.

    Returns
    -------
    list
        The most relevant documents for the given query, as returned by the
        underlying retriever.

    Examples
    --------
    >>> from guide_creator_flow.tools.custom_tool import RAGSearch
    >>> RAGSearch("Che cos'è la policy di rimborso?")  # doctest: +SKIP
    """
    retriever = initialize_vectorstore()
    results = retriever.invoke(query)
    return results
