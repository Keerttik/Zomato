import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"

# Create directories if they do not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
(SRC_DIR / "static").mkdir(parents=True, exist_ok=True)

# Database Configurations
DATABASE_PATH = DATA_DIR / "restaurants.db"

# LLM / API Configurations (Phase 3+)
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Ingestion configurations
DATASET_NAME = os.getenv("DATASET_NAME", "ManikaSaini/zomato-restaurant-recommendation")

# Recommendation defaults (Phase 2+)
CANDIDATE_LIMIT = int(os.getenv("CANDIDATE_LIMIT", 25))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", 5))
