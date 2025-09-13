import cv2
import mediapipe as mp
import pyttsx3
import time

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils
engine = pyttsx3.init()

# Suara English Male
voices = engine.getProperty('voices')
for v in voices:
    if "english" in v.name.lower() and "male" in v.name.lower():
        engine.setProperty('voice', v.id)
        break
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)

# Fungsi cek jari
def cek_jari(hand_landmarks):
    jari = []
    tip_ids = [4, 8, 12, 16, 20]
    for i in tip_ids:
        if hand_landmarks.landmark[i].y < hand_landmarks.landmark[i-2].y:
            jari.append(1)
        else:
            jari.append(0)
    return jari

# Kamus isyarat
gesture_dict = {
    (1,1,1,1,1): ("Halo!", "Hello!"),
    (0,1,0,0,0): ("Nama saya Rafka", "My name is Rafka"),
    (0,1,1,0,0): ("Saya sehat", "I am healthy"),
    (0,0,0,0,0): ("Apa kabar?", "How are you?"),
    (1,0,0,0,1): ("Sampai jumpa", "See you later"),
    (1,0,0,0,0): ("Mantap!", "Awesome!"),
    (0,1,1,1,1): ("Ayo belajar!", "Let's study!"),
    (1,1,0,0,0): ("Saya lapar", "I am hungry"),
}

# Stabilizer
last_gesture = None
gesture_count = 0
stable_gesture = None
last_speak_time = 0

while True:
    success, img = cap.read()
    if not success:
        print("Kamera tidak terbaca")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            jari = cek_jari(handLms)
            jari_tuple = tuple(jari)

            if jari_tuple in gesture_dict:
                if jari_tuple == last_gesture:
                    gesture_count += 1
                else:
                    gesture_count = 0
                last_gesture = jari_tuple

                # kalau gesture stabil 10 frame baru valid
                if gesture_count > 10:
                    stable_gesture = jari_tuple

    if stable_gesture:
        indo_text, eng_voice = gesture_dict[stable_gesture]
        cv2.putText(img, indo_text, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        now = time.time()
        if now - last_speak_time > 3:  # ngomong ulang tiap 3 detik
            print(f"👉 {indo_text}  |  🎤 {eng_voice}")
            engine.say(eng_voice)
            engine.runAndWait()
            last_speak_time = now

    cv2.imshow("Bahasa Isyarat AI", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
