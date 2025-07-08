import os
from pathlib import Path
from yt_dlp import YoutubeDL

def download_youtube_audio(url, output_path: Path) -> Path or None:
    """
    Downloads audio from a YouTube video and converts it to WAV.
    Returns the path to the saved .wav file or None on failure.
    """
    temp_audio_template = output_path.with_suffix(".%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(temp_audio_template),  # 🔧 CORRECT HERE
        'quiet': True,
        'ffmpeg_location': 'C:\\ffmpeg-7.1.1-full_build\\bin',  # 🔧 Your path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path = output_path.with_suffix('.wav')
        if final_path.exists():
            return final_path
        else:
            print("Expected .wav file was not found.")
            return None

    except Exception as e:
        print(f"YouTube download error: {e}")
        return None
