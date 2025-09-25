from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("AZURE_API_BASE")
subscription_key = os.getenv("AZURE_API_KEY")
api_version = os.getenv("AZURE_API_VERSION")

def get_embeddings() -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version,
    )

def get_llm():
    return AzureChatOpenAI(
        deployment_name="gpt-4o",
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version=api_version,
    )

