from gtts import gTTS
from tempfile import NamedTemporaryFile
import re
import os

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def text_to_audio(text: str):
    """
    Converts text to speech using gTTS and saves as an MP3.
    Returns (file_path, error) tuple.
    """
    try:
        text = clean_text(text)
        tts = gTTS(text=text, lang='en')

        with NamedTemporaryFile(delete=False, suffix=".mp3", mode='wb') as tmp:
            path = tmp.name
            tts.save(path)
        return path, None
    except Exception as e:
        return None, str(e)
