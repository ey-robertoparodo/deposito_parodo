from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("OPEN_API_KEY"),
    api_version=os.getenv("API_VERSION_EMBED")
)

response = client.embeddings.create(
    model="text-embedding-ada-002", 
    input="Ciao, come stai"
)

embedding_vector = response.data[0].embedding
print(f"Lunghezza embedding: {len(embedding_vector)}")
print(f"Primi 10 valori: {embedding_vector[:10]}")