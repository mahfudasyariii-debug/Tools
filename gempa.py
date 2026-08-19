import requests
import time
from datetime import datetime, timedelta

URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

last_event = None

print("=============================================")
print("       MONITOR GEMPA BMKG - REALTIME")
print("=============================================")
print("Polling setiap 2 detik...")
print("Tekan CTRL+C untuk berhenti.\n")


def ambil_data():
    try:
        r = requests.get(
            URL,
            timeout=10,
            headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "User-Agent": "GempaMonitor/1.0"
            }
        )

        r.raise_for_status()
        return r.json()["Infogempa"]["gempa"]

    except Exception as e:
        print(f"[ERROR] {e}")
        return None


def tampilkan(gempa):
    tanggal = gempa.get("Tanggal", "-")
    jam_wib = gempa.get("Jam", "-")

    # BMKG memberikan waktu dalam WIB.
    # Konversi ke WITA.
    try:
        dt = datetime.strptime(
            f"{tanggal} {jam_wib}",
            "%d %b %Y %H:%M:%S"
        )

        dt_wita = dt + timedelta(hours=1)
        waktu_wita = dt_wita.strftime("%d %b %Y %H:%M:%S WITA")

    except:
        waktu_wita = f"{tanggal} {jam_wib} WIB"

    print("\n=============================================")
    print("          GEMPA TERDETEKSI")
    print("=============================================")
    print(f"Tanggal    : {tanggal}")
    print(f"Jam        : {waktu_wita}")
    print(f"Magnitudo  : {gempa.get('Magnitude', '-')}")
    print(f"Kedalaman  : {gempa.get('Kedalaman', '-')}")
    print(f"Koordinat  : {gempa.get('Coordinates', '-')}")
    print(f"Wilayah    : {gempa.get('Wilayah', '-')}")
    print(f"Potensi    : {gempa.get('Potensi', '-')}")
    print(f"Dirasakan  : {gempa.get('Dirasakan', '-')}")
    print("=============================================")
    print("Sumber data: BMKG")
    print("=============================================\n")


# Ambil data pertama sebagai data awal.
# Supaya gempa lama tidak dianggap gempa baru.
gempa_awal = ambil_data()

if gempa_awal:
    last_event = (
        gempa_awal.get("Tanggal"),
        gempa_awal.get("Jam"),
        gempa_awal.get("Magnitude"),
        gempa_awal.get("Coordinates")
    )

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        f"Monitoring dimulai | Gempa terakhir: "
        f"{gempa_awal.get('Tanggal')} {gempa_awal.get('Jam')}"
    )
else:
    print("[START] Belum mendapatkan data BMKG.")


while True:
    gempa = ambil_data()

    if gempa:
        event_id = (
            gempa.get("Tanggal"),
            gempa.get("Jam"),
            gempa.get("Magnitude"),
            gempa.get("Coordinates")
        )

        if event_id != last_event:
            tampilkan(gempa)
            last_event = event_id

        else:
            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"Tidak ada gempa baru"
            )

    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"Gagal mengambil data"
        )

    time.sleep(2)