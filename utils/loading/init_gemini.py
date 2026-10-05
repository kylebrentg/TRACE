import os

from dotenv import load_dotenv
from google import genai


def initialize_gemini_api() -> genai.Client:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client
