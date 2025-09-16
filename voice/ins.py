import os
from gtts import gTTS

# Pastikan folder voices ada
os.makedirs("voices", exist_ok=True)

# List kata-kata/kalimat yang mau dibuat audio
texts = {
    "Emyu Stay du Goa": "Emyu Stay di goa",
    "Ini Adalah isyarat tangan dengan python": "Ini Adalah isyarat tangan dengan python",
  
}

# Generate audio file
for filename, text in texts.items():
    tts = gTTS(text=text, lang='id')  # 'id' = bahasa Indonesia
    path = f"voices/{filename}.mp3"
    tts.save(path)
    print(f"✅ {path} berhasil dibuat")
