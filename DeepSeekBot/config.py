import os
from dotenv import load_dotenv

load_dotenv()

AI_TOKEN = os.environ.get("AI_TOKEN")
TG_TOKEN = os.environ.get("TG_TOKEN")

if not AI_TOKEN or not TG_TOKEN:
    raise ValueError("AI_TOKEN or TG_TOKEN not found in environment variables.")