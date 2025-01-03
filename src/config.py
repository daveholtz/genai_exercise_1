import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
PASSWORD = os.getenv("PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# AI Model configurations
LEGACY_MODEL = "gpt-3.5-turbo-0125"
ADVANCED_MODEL = "gpt-4o-2024-08-06"

# File paths
ANSWERS_FILE = "answers.csv"
PLAYGROUND_FILE = "playground_interactions.json"

# Default AI parameters
DEFAULT_AI_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "presence_penalty": 0.1,
}
