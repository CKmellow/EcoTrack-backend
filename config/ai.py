# config/ai.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

INFLECTION_API_KEY = os.getenv("INFLECTION_API_KEY")

BASE_URL = "https://api.inflection.ai/v1"

def call_inflection(endpoint: str, payload: dict):
    headers = {
        "Authorization": f"Bearer {INFLECTION_API_KEY}",
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

