import requests
import time
import os
from datetime import datetime, timedelta

URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

last_event = None


# ============================================================
# STATUS SEMENTARA
# ============================================================

def status(teks):
    # Hapus seluruh isi baris sebelum menulis status baru
    print(f"\r\033[K{teks}", end="", flush=True)


# ============================================================
# AMBIL DATA BMKG
# ============================================================

def ambil_gempa():

    try:
        response = requests.get(
            URL,
            timeout=10,
            headers={
                "User-Agent": "GempaMonitor/1.0",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )

        response.raise_for_status()

        return response.json()["Infogempa"]["gempa"]

    except Exception:
        # Error tidak ditampilkan ke layar
        return None


# ============================================================
# TAMPILKAN GEMPA
# ============================================================

def tampilkan_gempa(gempa):

    tanggal = gempa.get("Tanggal", "-")
    jam = gempa.get("Jam", "-")

    # Waktu BMKG = WIB
    # WITA = WIB + 1 jam
    try:

        dt_wib = datetime.strptime(
            f"{tanggal} {jam}",
            "%d %b %Y %H:%M:%S"
        )

        dt_wita = dt_wib + timedelta(hours=1)

        waktu_bmkg = dt_wita.strftime(
            "%d %b %Y %H:%M:%S WITA"
        )

    except Exception:

        dt_wita = None
        waktu_bmkg = f"{tanggal} {jam}"

    # Waktu ketika tool menerima data
    waktu_terdeteksi = datetime.now()

    # Hitung delay
    if dt_wita:

        delay = waktu_terdeteksi - dt_wita
        delay_text = str(delay).split(".")[0]

    else:

        delay_text = "Tidak diketahui"


    # Pastikan status Monitoring sebelumnya selesai
    print("\r\033[K")

    # ========================================================
    # GEMPA PERMANEN
    # ========================================================

    print("=============================================")
    print("          GEMPA TERDETEKSI")
    print("=============================================")
    print()

    print(f"Waktu BMKG : {waktu_bmkg}")
    print(
        f"Terdeteksi : "
        f"{waktu_terdeteksi.strftime('%H:%M:%S')} WITA"
    )
    print(f"Delay      : {delay_text}")
    print()

    print(f"Magnitudo  : {gempa.get('Magnitude', '-')}")
    print(f"Kedalaman  : {gempa.get('Kedalaman', '-')}")
    print(f"Koordinat  : {gempa.get('Coordinates', '-')}")
    print(f"Wilayah    : {gempa.get('Wilayah', '-')}")
    print(f"Potensi    : {gempa.get('Potensi', '-')}")
    print(f"Dirasakan  : {gempa.get('Dirasakan', '-')}")

    print()
    print("=============================================")
    print("Sumber data: BMKG")
    print("=============================================")
    print()

    # Setelah gempa dicetak, monitoring kembali
    status(
        f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring..."
    )


# ============================================================
# START PROGRAM
# ============================================================

os.system("cls" if os.name == "nt" else "clear")

print("=============================================")
print("       MONITOR GEMPA BMKG - REALTIME")
print("=============================================")
print()
print("Status : TERHUBUNG")
print("Feed   : BMKG")
print("Polling: 2 detik")
print()
print("Menunggu gempa baru...")

status("[START] Mengambil data BMKG...")


# ============================================================
# DATA AWAL
# ============================================================

gempa_awal = ambil_gempa()

if gempa_awal:

    last_event = (
        gempa_awal.get("Tanggal"),
        gempa_awal.get("Jam"),
        gempa_awal.get("Magnitude"),
        gempa_awal.get("Coordinates")
    )


# Status awal
status(
    f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring..."
)


# ============================================================
# MONITOR REALTIME
# ============================================================

while True:

    gempa = ambil_gempa()

    if gempa:

        event_id = (
            gempa.get("Tanggal"),
            gempa.get("Jam"),
            gempa.get("Magnitude"),
            gempa.get("Coordinates")
        )

        # ====================================================
        # GEMPA BARU
        # ====================================================

        if event_id != last_event:

            tampilkan_gempa(gempa)

            last_event = event_id


    # ========================================================
    # STATUS MONITORING
    # ========================================================

    status(
        f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring..."
    )

    time.sleep(2)