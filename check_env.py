import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if key:
    print("Gemini API key found!")
else:
    print("API key not found. Check the variable name in .env.")