from fastapi import FastAPI, Request, HTTPException
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Fixed parameters
SAMPLE_COUNT = 1
PERSON_GENERATION = "allow"
ASPECT_RATIO = "16:9"

@app.post("/generate-image/")
async def generate_image(request: Request):
    try:
        payload = await request.json()
        prompt = payload.get('prompt')
        if not prompt:
            raise ValueError("Missing 'prompt' in request body.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
    headers = {'Content-Type': 'application/json'}

    data = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": SAMPLE_COUNT,
            "personGeneration": PERSON_GENERATION,
            "aspectRatio": ASPECT_RATIO,
        }
    }

    response = requests.post(f"{url}?key={GOOGLE_API_KEY}", headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
