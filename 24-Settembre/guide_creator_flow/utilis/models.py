from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("AZURE_API_BASE")
subscription_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")

def get_embeddings() -> AzureOpenAIEmbeddings:
    """Create and return an Azure OpenAI embeddings client.

    This convenience function initializes an `AzureOpenAIEmbeddings` instance
    using Azure configuration loaded from environment variables. The following
    variables are expected to be set prior to invocation:

    - `AZURE_API_BASE`: The Azure OpenAI endpoint base URL.
    - `AZURE_API_KEY`: The API key used for authentication.
    - `AZURE_API_VERSION`: The API version string.

    Returns
    -------
    AzureOpenAIEmbeddings
        A configured embeddings client that can be used by vector stores or
        other components requiring text embeddings.

    Raises
    ------
    EnvironmentError
        If any of the required environment variables is missing.

    Examples
    --------
    >>> from utilis.models import get_embeddings
    >>> embeddings = get_embeddings()
    >>> vectors = embeddings.embed_documents(["hello world"])  # doctest: +SKIP
    """
    if not (endpoint and subscription_key and api_version):
        raise EnvironmentError(
            "Missing Azure configuration. Ensure AZURE_API_BASE, AZURE_API_KEY, and AZURE_API_VERSION are set."
        )
    return AzureOpenAIEmbeddings(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version,
    )

def get_llm():
    """Create and return an Azure Chat LLM client.

    Initializes an `AzureChatOpenAI` client configured with the deployment
    `gpt-4o` and Azure credentials from environment variables.

    Returns
    -------
    AzureChatOpenAI
        A chat-completion capable LLM client for generating responses.

    Raises
    ------
    EnvironmentError
        If any of the required environment variables is missing.

    Examples
    --------
    >>> from utilis.models import get_llm
    >>> llm = get_llm()
    >>> llm.invoke("Say hello")  # doctest: +SKIP
    """
    if not (endpoint and subscription_key and api_version):
        raise EnvironmentError(
            "Missing Azure configuration. Ensure AZURE_API_BASE, AZURE_API_KEY, and AZURE_API_VERSION are set."
        )
    return AzureChatOpenAI(
        deployment_name="gpt-4o",
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version,
    )

