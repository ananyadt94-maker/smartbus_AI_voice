from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
user_message = input("Enter your bus journey: ")
prompt = f"""
You are the AI assistant for SmartBus Assist.

Understand the user's bus journey request.

Extract:
1. intent
2. source
3. destination
4. language

Return ONLY valid JSON in this format:

{{
    "intent": "find_route",
    "source": "CMRIT",
    "destination": "Majestic",
    "language": "English"
}}

If the source or destination is missing, use null.
Do not invent locations.

User message: {user_message}
"""

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    print("Gemini connection successful!")
    print(response.text)

except Exception as error:
    print("Error:", error)