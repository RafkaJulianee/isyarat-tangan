import cv2
import mediapipe as mp
import numpy as np
from gtts import gTTS
import os
import time
from sklearn.neighbors import KNeighborsClassifier

# === Setup MediaPipe ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# === Dataset sederhana (contoh gesture) ===
X_train = [
    [1,1,1,1,1],   # ✋ semua jari
    [0,0,0,0,0],   # ✊ kepalan
    [0,1,0,0,0],   # 👉 telunjuk
    [0,1,1,0,0],   # ✌️ peace
    [1,0,0,0,0],   # 👍 jempol
    [1,0,0,0,1],   # 🤙 jempol+kelingking
    [0,1,0,0,1],   # 🤘 rock
    [0,1,1,1,0],   # 🖖 scout
    [0,0,1,0,0],   # 🖕 tengah aja
    [1,1,0,0,0],   # 👌 oke
]
y_train = [
    "Halo, apa kabar?",
    "Saya baik-baik saja",
    "Nama saya Rafka",
    "Terima kasih",
    "Bagus!",
    "Sampai jumpa",
    "Ayo semangat!",
    "Salam kenal",
    "Jangan marah dong",
    "Oke sip"
]

# Latih model KNN
clf = KNeighborsClassifier(n_neighbors=1)
clf.fit(X_train, y_train)

# === Kamera ===
cap = cv2.VideoCapture(0)

last_text = ""
last_time = 0

def cek_jari(hand_landmarks):
    jari = []
    tip_ids = [4, 8, 12, 16, 20]
    for i in tip_ids:
        if hand_landmarks.landmark[i].y < hand_landmarks.landmark[i-2].y:
            jari.append(1)
        else:
            jari.append(0)
    return jari

def play_tts(text):
    global last_text, last_time
    if text != last_text or (time.time() - last_time) > 3:  # biar ga spam
        tts = gTTS(text=text, lang='id')
        filename = "voice.mp3"
        tts.save(filename)
        os.system(f"start {filename}")  # Windows
        last_text = text
        last_time = time.time()

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            jari = cek_jari(handLms)

            if len(jari) == 5:
                gesture = clf.predict([jari])[0]
                cv2.putText(img, gesture, (50,100), cv2.FONT_HERSHEY_SIMPLEX,
                            1.2, (0,255,0), 3)
                play_tts(gesture)

    cv2.imshow("Bahasa Isyarat", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
