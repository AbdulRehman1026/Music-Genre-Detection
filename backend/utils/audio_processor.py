import librosa
import numpy as np

def process_audio_and_predict(file_path, model):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        y = y[:660000]  # 30 seconds max
        mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_db = librosa.power_to_db(mel, ref=np.max)

        mel_db = np.expand_dims(mel_db, axis=-1)
        mel_db = np.expand_dims(mel_db, axis=0)

        prediction = model.predict(mel_db)
        predicted_class = np.argmax(prediction, axis=1)[0]

        genre_labels = ['blues', 'classical', 'country', 'disco', 'hiphop',
                        'jazz', 'metal', 'pop', 'reggae', 'rock']
        return genre_labels[predicted_class]
    except Exception as e:
        return f"Error: {str(e)}"
