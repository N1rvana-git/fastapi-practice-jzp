from pydantic_settings import BaseSettings,SettingsConfigDict
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env" #path是config文件路径，src/目录-根目录-拼接虚拟环境

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8"
    )
    APP_NAME:str="默认fastapi应用"
    ENVIRONMENT:str="development"
    DATABASE_URL:str="sqlite+aiosqlite:///./test.db"# Pydantic 会自动从 .env 读取它

settings = Settings()