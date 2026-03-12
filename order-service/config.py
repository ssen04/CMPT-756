import os


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.db_host = os.getenv("DB_HOST", "127.0.0.1")
        self.db_port = int(os.getenv("DB_PORT", "3306"))
        self.db_name = os.getenv("DB_NAME", "ecomm_db")
        self.db_user = os.getenv("DB_USER", "test")
        self.db_password = os.getenv("DB_PASSWORD", "Canada@2021")


settings = Settings()
