"""import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def analyze_bug(prompt: str):

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    return response.text
"""


def analyze_bug(prompt: str):

    return """
    {
        "severity": "High",
        "priority": "P1",
        "component": "Authentication",
        "confidence": "95%",
        "reasoning": "The application crashes during the login process."
    }
    """
