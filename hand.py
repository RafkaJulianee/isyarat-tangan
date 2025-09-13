import cv2
import mediapipe as mp
import time
from playsound import playsound
import threading

# Buka modul mediapipe tangan
tangan_mp = mp.solutions.hands
gambar_mp = mp.solutions.drawing_utils
deteksi_tangan = tangan_mp.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Buat ngatur biar suara gak keulang-ulang terus
suara_terakhir = None
waktu_terakhir = 0

# Fungsi buat muter suara (pake thread biar gak bikin aplikasi nge-freeze)
def putar_suara(file):
    def _mainkan():
        playsound(f"voice/{file}")
    threading.Thread(target=_mainkan).start()

# Fungsi buat cek gaya tangan (gesture)
def cek_gaya_tangan(titik_tangan):
    # Id ujung jari (telunjuk, tengah, manis, kelingking)
    ujung_jari = [8, 12, 16, 20]
    sendi_jari = [6, 10, 14, 18]

    status_jari = []
    for ujung, sendi in zip(ujung_jari, sendi_jari):
        # Kalo posisi ujung jari lebih tinggi dari sendinya → dianggap ngacung
        status_jari.append(titik_tangan.landmark[ujung].y < titik_tangan.landmark[sendi].y)

    # Cek jempol (pakai sumbu x karena arahnya beda)
    jempol = titik_tangan.landmark[4].x < titik_tangan.landmark[3].x

    # Gerakan Tangan
    if all(status_jari):
        return "my_name_is_rafka julian.mp3"   # Semua jari terbuka
    elif status_jari[0] and not any(status_jari[1:]):
        return "salam_kenal.mp3"               # Cuma telunjuk
    elif jempol and not any(status_jari):
        return "hello_world.mp3"               # Cuma jempol
    elif jempol and status_jari[3] and not status_jari[0:3]:
        return "apa_kabar.mp3"           # Jempol + kelingking
    elif status_jari[0] and status_jari[1] and not status_jari[2:] and not jempol:
        return "setia.mp3"                     # Telunjuk + tengah
    else:
        return None

# Nyalain kamera
kamera = cv2.VideoCapture(0)

while kamera.isOpened():
    ret, frame = kamera.read()
    if not ret:
        break

    # Biar mediapipe bisa baca (ubah jadi RGB)
    gambar_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hasil = deteksi_tangan.process(gambar_rgb)

    # Kalau ada tangan ketangkep kamera
    if hasil.multi_hand_landmarks:
        for titik_tangan in hasil.multi_hand_landmarks:
            gambar_mp.draw_landmarks(frame, titik_tangan, tangan_mp.HAND_CONNECTIONS)

            gaya = cek_gaya_tangan(titik_tangan)

            if gaya:
                # Kasih jeda 2 detik biar suara gak spam
                if gaya != suara_terakhir or time.time() - waktu_terakhir > 2:
                    putar_suara(gaya)
                    suara_terakhir = gaya
                    waktu_terakhir = time.time()

                # Tulis teks nama gaya di layar
                cv2.putText(frame, gaya.replace(".mp3", ""), (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Deteksi Gaya Tangan", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC buat keluar
        break

kamera.release()
cv2.destroyAllWindows()
