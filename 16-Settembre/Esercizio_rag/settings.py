from dataclasses import dataclass

@dataclass
class Settings:
    # Persistenza FAISS
    persist_dir: str = "faiss_index_example"
    # Text splitting
    chunk_size: int = 2000
    chunk_overlap: int = 400
    # Retriever (MMR)
    search_type: str = "mmr"  # "mmr" o "similarity"
    k: int = 4  # risultati finali
    fetch_k: int = 20  # candidati iniziali (per MMR)
    mmr_lambda: float = 0.3  # 0 = diversificazione massima, 1 = pertinenza massima
    # Embedding
    hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    # LM Studio (OpenAI-compatible)
    lmstudio_model_env: str = (
        "LMSTUDIO_MODEL"  # nome del modello in LM Studio, via env var
    )