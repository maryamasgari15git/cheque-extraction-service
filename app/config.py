import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

SERVICE_API_KEY = os.getenv("SERVICE_API_KEY")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
REQUEST_TIMEOUT_SECONDS = 30
MODEL_TIMEOUT_SECONDS = 30