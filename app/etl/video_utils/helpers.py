import requests

from app.config.settings import Gemini
from google import genai
from google.genai import types

client = genai.Client(api_key=Gemini.GEMINI_API_KEY)
session = requests.session()

def call_gemini(prompt):
    response = client.models.generate_content(
        model=Gemini.MODEL_ID,
        contents=Gemini.SYSTEM_PROMPT + "\n\n" + prompt,
        config=types.GenerateContentConfig(
            temperature=0
        ),
    )
    return response


def detect_short(video_id):
    url = f"https://www.youtube.com/shorts/{video_id}"

    try:
        resp = session.head(url, allow_redirects=True, timeout=10)

        if "/shorts/" in resp.url:
            return "Short"
        return "Regular"

    except requests.RequestException:
        return "Unknown"

