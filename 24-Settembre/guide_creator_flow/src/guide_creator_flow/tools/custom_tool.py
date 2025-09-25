from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai.tools import tool

from utilis.db_vet import initialize_vectorstore

@tool("RAGSearch")
def RAGSearch(query: str) -> str:
    """
    This tool performs a similarity search on a vector store using the provided query and returns the top 5 relevant documents.

    Parameters:
    - query (str): The search query string.

    Returns:
    - List[Document]: A list of the top 5 documents most similar to the query
    """
    retriever = initialize_vectorstore()
    results = retriever.invoke(query)
    return results
