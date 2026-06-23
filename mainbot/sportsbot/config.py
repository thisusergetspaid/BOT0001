import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")

SPORTS_API_BASE_URL = os.getenv("SPORTS_API_BASE_URL")
