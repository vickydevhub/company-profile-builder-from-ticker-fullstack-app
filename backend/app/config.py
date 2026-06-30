from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    STUB_BASE_URL = os.getenv("STUB_BASE_URL")
    API_PREFIX = os.getenv("API_PREFIX", "/api")

settings = Settings()