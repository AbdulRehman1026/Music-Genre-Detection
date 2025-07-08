import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

def predict_from_file(audio_file):
    if audio_file is None:
        return "No audio file provided."

    with open(audio_file, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/predict/file", files=files)

    if response.status_code == 200:
        return f"🎧 Genre: {response.json()['genre']}"
    else:
        return f"❌ Error: {response.text}"

def predict_from_youtube(url):
    if not url:
        return "YouTube URL is empty."

    data = {"url": url}
    response = requests.post(f"{API_URL}/predict/youtube", data=data)

    if response.status_code == 200:
        return f"🎧 Genre: {response.json()['genre']}"
    else:
        return f"❌ Error: {response.text}"

def predict_from_mic(audio_file):
    if audio_file is None:
        return "No mic input recorded."

    with open(audio_file, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/predict/mic", files=files)

    if response.status_code == 200:
        return f"🎧 Genre: {response.json()['genre']}"
    else:
        return f"❌ Error: {response.text}"

# Gradio Interfaces

file_upload_tab = gr.Interface(
    fn=predict_from_file,
    inputs=gr.Audio(type="filepath", label="🎵 Upload Audio File"),
    outputs="text",
    title="🎶 Music Genre Detection (File Upload)",
)

mic_record_tab = gr.Interface(
    fn=predict_from_mic,
    inputs=gr.Audio(type="filepath", label="🎵 Upload Audio File"),
    outputs="text",
    title="🎶 Music Genre Detection (Mic)",
)

youtube_tab = gr.Interface(
    fn=predict_from_youtube,
    inputs=gr.Textbox(label="🔗 YouTube Link", placeholder="Paste a YouTube link here..."),
    outputs="text",
    title="🎶 Music Genre Detection (YouTube Link)",
)

# Combine into tabs
gr.TabbedInterface(
    [file_upload_tab, mic_record_tab, youtube_tab],
    ["📁 File Upload", "🎤 Microphone", "🔗 YouTube Link"]
).launch()
