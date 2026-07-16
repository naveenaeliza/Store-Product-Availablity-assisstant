import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MCP Transport Configuration: "sse" or "stdio"
    MCP_TRANSPORT: str = "stdio"
    
    # SSE Connection Configuration
    MCP_SSE_URL: str = "http://localhost:8000/sse"

    # STDIO Process Configuration
    MCP_STDIO_COMMAND: str = str(
        Path(__file__).resolve().parents[1]
        / ".venv"
        / "Scripts"
        / "python.exe"
    )
    MCP_STDIO_ARGS: list[str] = [
        str(
            Path(__file__).resolve().parents[1]
            / "backend"
            / "server.py"
        )
    ]

    # Env variables required by backend if run via STDIO
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
