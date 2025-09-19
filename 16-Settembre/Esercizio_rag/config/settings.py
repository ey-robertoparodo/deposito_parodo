from dataclasses import dataclass

@dataclass
class Settings:
    persist_dir: str = "faiss_index_example"
    chunk_size: int = 2000
    chunk_overlap: int = 400
    search_type: str = "mmr" 
    k: int = 4 
    fetch_k: int = 20
    mmr_lambda: float = 0.3