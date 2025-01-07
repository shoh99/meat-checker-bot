import os

from dotenv import load_dotenv
from os import getenv
from pathlib import Path


class Config:
    """Configuration class to handle environment variables and constants."""
    load_dotenv()

    def __init__(self):
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
        self.NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
        self.GROQ_API_KEY = os.getenv('GROQ_API')
        self.CONNECTION_STRING = os.getenv('CONNECTION_STRING')
        self.DB_NAME = os.getenv('DB_NAME')
        # Validate required environment variables
        self._validate_config()

        # Create media directory if it doesn't exist
        self.MEDIA_DIR = Path("media")
        # self.MEDIA_DIR.mkdir(exist_ok=True)

    def _validate_config(self):
        """Validate that all required environment variables are set."""
        required_vars = {
            'BOT_TOKEN': self.BOT_TOKEN,
            'NAVER_CLIENT_ID': self.NAVER_CLIENT_ID,
            'NAVER_CLIENT_SECRET': self.NAVER_CLIENT_SECRET,
            'GROQ_API_KEY': self.GROQ_API_KEY,
            'CONNECTION_STRING': self.CONNECTION_STRING,
            'DB_NAME': self.DB_NAME
        }

        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
