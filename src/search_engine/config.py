"""
Centralized configuration loader.
Reads required environment variables and fails fast with a clear
error if any are missing, rather than letting a downstream API call
fail with a cryptic error.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    @classmethod
    def validate(cls) -> None:
        """Raise a clear error if any required config value is missing."""
        missing = [
            name
            for name, value in {
                "TAVILY_API_KEY": cls.TAVILY_API_KEY,
                "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            }.items()
            if not value
        ]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Check your .env file against .env.example."
            )


config = Config()