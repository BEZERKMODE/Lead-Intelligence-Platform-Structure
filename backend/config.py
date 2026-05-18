import os
from dotenv import load_dotenv

# Load .env variables from the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lead-intel-super-secret-key-1234')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # AI and Enrichment settings
    MOCK_AI_RESPONSE_DELAY = 1.0  # seconds
    MOCK_CRAWLER_DELAY = 0.5      # seconds
    
    # Scoring configurations
    SCORING_WEIGHT_TECH = 0.35
    SCORING_WEIGHT_GROWTH = 0.35
    SCORING_WEIGHT_SIZE = 0.30
    
    # Apollo.io API configuration key
    APOLLO_API_KEY = os.environ.get('APOLLO_API_KEY', '')
