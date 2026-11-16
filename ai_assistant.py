
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load the API key from Backend/.env
load_dotenv(Path(__file__).with_name(".env"))

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_journey(user_message):

    prompt = f"""
    You are the AI assistant for SmartBus Assist.

    Understand the user's bus journey request.

    Extract:
    1. intent:
       - find_route
       - sos
       - where_am_i
       - stops_remaining
       - destination_alert
       - repeat_instruction
       - help

    2. source: Starting location, or null.
    3. destination: Ending location, or null.
    4. language: English, Kannada, or Hindi.

    Return ONLY valid JSON with these keys:
    intent, source, destination, language.

    Never invent locations.

    User message: {user_message}
    """

    result = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return json.loads(result.text)


def generate_response(language, source, destination):

    prompt = f"""
    You are the voice assistant for SmartBus Assist.

    Reply briefly in {language}.

    Tell the passenger that you are checking their
    journey from {source} to {destination}.

    Do not invent bus numbers, timings or routes.
    """

    result = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return result.text.strip()


def process_voice_request(user_message):

    journey = extract_journey(user_message)

    if journey["intent"] == "sos":
        return {
            "intent": "sos",
            "message": "Emergency assistance requested."
        }

    if journey["intent"] == "find_route":

        if not journey["source"] or not journey["destination"]:
            return {
                "intent": "find_route",
                "message": "Please provide your starting point and destination."
            }

        reply = generate_response(
            journey["language"],
            journey["source"],
            journey["destination"]
        )

        return {
            "intent": "find_route",
            "source": journey["source"],
            "destination": journey["destination"],
            "language": journey["language"],
            "message": reply
        }

    return journey
