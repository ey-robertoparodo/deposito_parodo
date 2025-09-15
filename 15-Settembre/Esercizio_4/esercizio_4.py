from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Configurazione client Azure
client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("OPEN_API_KEY"),
    api_version="2023-05-15"
)

response = client.embeddings.create(
    model="text-embedding-ada-002", 
    input="Ciao, come stai"
)

embedding_vector = response.data[0].embedding
print(f"Lunghezza embedding: {len(embedding_vector)}")
print(f"Primi 10 valori: {embedding_vector[:10]}")