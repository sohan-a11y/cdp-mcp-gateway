from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CHROME_CDP_URL: str = "http://localhost:9222"
    MCP_SERVER_NAME: str = "cdp-mcp-gateway"
    LOG_LEVEL: str = "INFO"
    ACTION_TIMEOUT: int = 15

    class Config:
        env_file = ".env"

settings = Settings()
