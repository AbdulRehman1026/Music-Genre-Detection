from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from utils.audio_processor import process_audio_and_predict
from utils.youtube_downloader import download_youtube_audio
import os
import shutil
import uuid

# Initialize FastAPI app
app = FastAPI()

# Enable CORS so frontend (Gradio) can access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once at startup
model = load_model("model/genre_model.h5", compile=False)

# Create temp folder if not exists
os.makedirs("temp", exist_ok=True)

@app.post("/predict/file")
async def predict_from_file(file: UploadFile = File(...)):
    temp_path = f"temp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    prediction = process_audio_and_predict(temp_path, model)
    os.remove(temp_path)

    return JSONResponse({"genre": prediction})


@app.post("/predict/youtube")
async def predict_from_youtube(url: str = Form(...)):
    audio_path = download_youtube_audio(url)
    if not audio_path:
        return JSONResponse({"error": "Failed to download YouTube audio."}, status_code=400)

    prediction = process_audio_and_predict(audio_path, model)
    os.remove(audio_path)

    return JSONResponse({"genre": prediction})


@app.post("/predict/mic")
async def predict_from_mic(file: UploadFile = File(...)):
    temp_path = f"temp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    prediction = process_audio_and_predict(temp_path, model)
    os.remove(temp_path)

    return JSONResponse({"genre": prediction})
