from pytube import YouTube
from datetime import datetime
import uuid
import whisper
from langdetect import detect
import requests
import os

def transcribe_video(file_path) -> str:
    # Load the model
    model = whisper.load_model("base")

    # Transcribe an audio file
    result = model.transcribe(file_path)

    return result


def translate_text(text, target_language="en"):
    url = "https://translation.googleapis.com/language/translate/v2"

    # Set the parameters for the API request
    params = {
        "q": text,
        "target": target_language,
        "key": os.getenv("GOOGLE_TRANSLATE_API_KEY")
    }

    # Make the API request
    response = requests.post(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        translated_text = result['data']['translations'][0]['translatedText']
        print(f"Original text: {text}")
        print(f"Translated text: {translated_text}")
        return response.status_code, translated_text
    else:
        return response.status_code, ""


def detect_language(text):
    language = detect(text)
    print(f"The detected language is: {language}")
    return language


def download_youtube_video(url, output_path='.'):
    global downloaded_file_path, yt
    try:
        # object creation using YouTube
        yt = YouTube(url)
    except:
        # to handle exception
        print("Connection Error")

    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4').get_highest_resolution()

    try:
        # downloading the video
        downloaded_file_path = mp4_streams.download(output_path=output_path)
        print('Video downloaded successfully!')
    except Exception as e:
        print(f"An error occurred: {e}")
    # Return the path where the video was downloaded
    return downloaded_file_path


def prepare_data(docs, link):
    metadata = []
    ids = []
    for i, chunk in enumerate(docs):
        uuid4 = uuid.uuid4()
        metadata.append({
            "text": chunk,
            "doc_id": str(uuid4),
            "video": link,
            "timestamp": datetime.now().isoformat()
        })
        ids.append(f"id={uuid4}")
        return metadata, ids
