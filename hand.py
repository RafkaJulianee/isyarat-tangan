import cv2
import mediapipe as mp
import time
from playsound import playsound
import threading

# pake mediapipe buat deteksi tangan
tangan = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
gambar = mp.solutions.drawing_utils

suara_terakhir = None
waktu_terakhir = 0

def putar_suara(file):
    def jalan():
        playsound(f"voice/{file}")
    threading.Thread(target=jalan).start()

def cek_gaya(titik):
    ujung = [8, 12, 16, 20]
    sendi = [6, 10, 14, 18]
    jari = [titik.landmark[u].y < titik.landmark[s].y for u, s in zip(ujung, sendi)]
    jempol = titik.landmark[4].x < titik.landmark[3].x

    if all(jari): return "my_name_is_rafka julian.mp3"
    if jari[0] and not any(jari[1:]): return "salam_kenal.mp3"
    if jempol and not any(jari): return "hello_world.mp3"
    if jempol and jari[3] and not jari[0:3]: return "nama_saya_rafka.mp3"
    if jari[0] and jari[1] and not jari[2:] and not jempol: return "setia.mp3"
    return None

kamera = cv2.VideoCapture(0)

while kamera.isOpened():
    ret, frame = kamera.read()
    if not ret: break

    hasil = tangan.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if hasil.multi_hand_landmarks:
        for titik in hasil.multi_hand_landmarks:
            gambar.draw_landmarks(frame, titik, mp.solutions.hands.HAND_CONNECTIONS)

            gaya = cek_gaya(titik)
            if gaya and (gaya != suara_terakhir or time.time() - waktu_terakhir > 2):
                putar_suara(gaya)
                suara_terakhir, waktu_terakhir = gaya, time.time()
                cv2.putText(frame, gaya.replace(".mp3", ""), (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gaya Tangan", frame)
    if cv2.waitKey(1) & 0xFF == 27: break  # ESC keluar

kamera.release()
cv2.destroyAllWindows()
