from fastapi import FastAPI
import os
import requests
import base64
import io
from PIL import Image
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class ImageRequest(BaseModel):
    prompt: str
    sampleCount: int = 1
    personGeneration: str = "allow"
    aspectRatio: str = "16:9"

@app.post("/generate-image")
def generate_image(request: ImageRequest):
    url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
    headers = {'Content-Type': 'application/json'}

    data = {
        "instances": [{"prompt": request.prompt}],
        "parameters": {
            "sampleCount": request.sampleCount,
            "personGeneration": request.personGeneration,
            "aspectRatio": request.aspectRatio,
        }
    }

    response = requests.post(f"{url}?key={GOOGLE_API_KEY}", headers=headers, json=data)

    if response.status_code != 200:
        return {"error": response.json()}

    return response.json()
