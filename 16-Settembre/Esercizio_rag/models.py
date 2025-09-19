from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_embeddings() -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("OPEN_API_KEY"),
        api_version=os.getenv("API_VERSION_EMBED"),
    )


def get_llm():
    return AzureChatOpenAI(
        deployment_name="gpt-4o",
        api_version=os.getenv("API_VERSION"),
        azure_endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("OPEN_API_KEY"),
    )