from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.1:8b"
    ollama_embed_model: str = "nomic-embed-text"

    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_local_path: str = "./qdrant_storage"

    # Logfire
    logfire_token: str | None = None

    # Application Settings
    chunk_size: int = 512
    chunk_overlap: int = 50
    bm25_weight: float = 0.4
    qdrant_weight: float = 0.6
    confidence_threshold: float = 0.7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
