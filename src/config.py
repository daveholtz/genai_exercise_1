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

# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# File paths (now S3 key prefixes)
ANSWERS_PREFIX = "answers/"
PLAYGROUND_PREFIX = "playground/"

# Default AI parameters
DEFAULT_AI_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "presence_penalty": 0.1,
}
