import yt_dlp
import os
import uuid
from pydub import AudioSegment

def download_youtube_audio(url):
    temp_id = str(uuid.uuid4())
    temp_mp3 = f"temp/{temp_id}.mp3"
    temp_wav = f"temp/{temp_id}.wav"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_mp3,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        audio = AudioSegment.from_mp3(temp_mp3)
        audio.export(temp_wav, format="wav")
        os.remove(temp_mp3)
        return temp_wav
    except Exception as e:
        print("YouTube download error:", e)
        return None
