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
    GOOGLE_SEARCH_API_KEY: str = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    @classmethod
    def validate(cls) -> None:
        """Raise a clear error if any required config value is missing."""
        missing = [
            name
            for name, value in {
                "GOOGLE_SEARCH_API_KEY": cls.GOOGLE_SEARCH_API_KEY,
                "GOOGLE_CSE_ID": cls.GOOGLE_CSE_ID,
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