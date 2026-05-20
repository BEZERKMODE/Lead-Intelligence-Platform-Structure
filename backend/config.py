import os

from dotenv import load_dotenv

load_dotenv()

class Settings:

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/lead_db"
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    JWT_SECRET = os.getenv(
        "JWT_SECRET",
        "super-secret-key"
    )

    JWT_ALGORITHM = "HS256"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

    ZEROBOUNCE_API_KEY = os.getenv("ZEROBOUNCE_API_KEY")

    HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

settings = Settings()
