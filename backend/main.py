from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
from pathlib import Path
import numpy as np
import uvicorn
import os
import uuid
from utils.audio_processor import extract_features
from utils.youtube_downloader import download_youtube_audio

# Load model
model = load_model("model/genre_model.h5", compile=False)

# Class labels
CLASS_NAMES = [
    "blues", "classical", "country", "disco", "hiphop",
    "jazz", "metal", "pop", "reggae", "rock"
]

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def predict_genre(audio_path: Path, model) -> str:
    predictions = extract_features(audio_path, model)
    predicted_index = np.argmax(predictions)
    return CLASS_NAMES[predicted_index]

@app.post("/predict/file")
async def predict_from_file(file: UploadFile = File(...)):
    try:
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_file_path = temp_dir / f"{uuid.uuid4().hex}_{file.filename}"
        
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        genre = predict_genre(temp_file_path, model)
        os.remove(temp_file_path)
        return {"genre": genre}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/youtube")
async def predict_from_youtube(url: str = Form(...)):
    try:
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_filename = f"{uuid.uuid4().hex}.wav"
        output_path = temp_dir / temp_filename

        audio_path = download_youtube_audio(url, output_path)

        if not audio_path or not audio_path.exists():
            raise HTTPException(status_code=400, detail="Failed to download audio.")

        genre = predict_genre(audio_path, model)
        os.remove(audio_path)
        return {"genre": genre}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YouTube prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
