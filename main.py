from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Fixed parameters
SAMPLE_COUNT = 1
PERSON_GENERATION = "allow"
ASPECT_RATIO = "16:9"

# Define a request model
class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
    headers = {'Content-Type': 'application/json'}

    data = {
        "instances": [{"prompt": request.prompt}],
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
