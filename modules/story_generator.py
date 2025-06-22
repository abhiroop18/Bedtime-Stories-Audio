import requests
import streamlit as st
import os


# Load API Key from .env


HF_TOKEN = st.secrets["api"]["huggingface_token"]

def generate_story(name: str, age: int, hobbies: str, tone: str) -> str:
    prompt = (
        f"Write a short bedtime story for a child named {name}, who is {age} years old and loves {hobbies}. "
        f"The story should be {tone.lower()} and end with a simple moral. Use simple language for a child"
    )

    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"].replace(prompt, "").strip()
        else:
            return f"❌ Error: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"
