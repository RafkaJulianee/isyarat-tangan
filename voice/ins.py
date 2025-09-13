import os
from gtts import gTTS

# Pastikan folder voices ada
os.makedirs("voices", exist_ok=True)

# List kata-kata/kalimat yang mau dibuat audio
texts = {
    "hello_world": "Hello world!",
    "my_name_is_rafka Julian": "My Name is Rafka Julian",
    "salam_kenal": "Salam Kenal Ya",
    "apa_kabar": "Apa kabar?",
    "baiklah": "Baiklah"
}

# Generate audio file
for filename, text in texts.items():
    tts = gTTS(text=text, lang='id')  # 'id' = bahasa Indonesia
    path = f"voices/{filename}.mp3"
    tts.save(path)
    print(f"✅ {path} berhasil dibuat")
