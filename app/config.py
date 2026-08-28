"""应用配置"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # LLM
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"

    # Search
    search_api_provider: str = "tavily"
    tavily_api_key: str = ""

    # App
    app_host: str = "127.0.0.1"
    app_port: int = 3001
    database_url: str = "sqlite:///./data/cache.db"
    cache_ttl_hours: int = 24
    max_products: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

# 确保 data 目录存在
Path("data").mkdir(exist_ok=True)

