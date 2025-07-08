import librosa
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import os
import uuid

def extract_features(file_path, model, img_height=128, img_width=130):
    try:
        # Load audio file
        y, sr = librosa.load(file_path, duration=30)

        # Generate mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)

        # Save spectrogram as image
        temp_img_path = f"temp/{uuid.uuid4().hex}.png"
        plt.figure(figsize=(img_width / 100, img_height / 100))
        plt.axis('off')
        plt.imshow(S_dB, aspect='auto', origin='lower')
        plt.tight_layout(pad=0)
        plt.savefig(temp_img_path, bbox_inches='tight', pad_inches=0)
        plt.close()

        # Load image and resize (PIL)
        img = Image.open(temp_img_path).convert("RGB")
        img = img.resize((img_width, img_height))
        img_array = img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # ✂️ Removed os.remove(temp_img_path) — we now keep the spectrogram image

        # Predict genre
        prediction = model.predict(img_array)
        return prediction
    
    except Exception as e:
        raise RuntimeError(f"Prediction failed for {file_path}: {str(e)}")
