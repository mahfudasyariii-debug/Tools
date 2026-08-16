import cv2
import time

# Ganti dengan alamat IP Webcam HP kamu
URL = "http://IP_HP:PORT/video"

camera = cv2.VideoCapture(URL)

if not camera.isOpened():
    print("[-] Kamera tidak bisa terhubung!")
    exit()

print("[+] Kamera terhubung!")
print("[+] Motion detector aktif...")
print("[+] Tekan Ctrl+C untuk berhenti.")

previous = None
last_detection = 0

while True:
    success, frame = camera.read()

    if not success:
        print("[-] Frame gagal dibaca!")
        break

    # Ubah gambar menjadi grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Kurangi detail kecil/noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Frame pertama hanya dijadikan acuan
    if previous is None:
        previous = gray
        continue

    # Bandingkan frame sekarang dengan frame sebelumnya
    difference = cv2.absdiff(previous, gray)

    # Hitung seberapa besar perubahan
    _, threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

    changed_pixels = cv2.countNonZero(threshold)

    # Kalau perubahan cukup besar
    if changed_pixels > 5000:

        current_time = time.time()

        # Supaya tidak spam terus-menerus
        if current_time - last_detection > 2:
            print("[DETECTION!] Ada gerakan!")
            last_detection = current_time

    previous = gray

camera.release()