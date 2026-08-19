#!/usr/bin/env python3

import json
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Module requests belum terpasang.")
    print("Install dengan: pip install requests")
    raise SystemExit(1)


API_URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
INTERVAL = 60


def waktu_sekarang():
    return datetime.now().strftime("%H:%M:%S")


def ambil_data():
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"[{waktu_sekarang()}] Gagal mengambil data: {e}")
        return None

    except json.JSONDecodeError:
        print(f"[{waktu_sekarang()}] Respons BMKG bukan JSON yang valid.")
        return None


def tampilkan_gempa(gempa):
    print()
    print("=" * 45)
    print("          GEMPA TERDETEKSI")
    print("=" * 45)

    print(f"Tanggal    : {gempa.get('Tanggal', '-')}")
    print(f"Jam        : {gempa.get('Jam', '-')}")
    print(f"Magnitudo  : {gempa.get('Magnitude', '-')}")
    print(f"Kedalaman  : {gempa.get('Kedalaman', '-')}")
    print(f"Koordinat  : {gempa.get('Lintang', '-')} "
          f"{gempa.get('Bujur', '-')}")
    print(f"Wilayah    : {gempa.get('Wilayah', '-')}")
    print(f"Potensi    : {gempa.get('Potensi', '-')}")
    print(f"Dirasakan  : {gempa.get('Dirasakan', '-')}")
    print("=" * 45)
    print("Sumber data: BMKG")


def identitas_gempa(gempa):
    """
    Membuat identitas sederhana agar gempa yang sama
    tidak dianggap sebagai gempa baru setiap menit.
    """
    return (
        gempa.get("DateTime")
        or (
            gempa.get("Tanggal", ""),
            gempa.get("Jam", ""),
            gempa.get("Magnitude", ""),
            gempa.get("Lintang", ""),
            gempa.get("Bujur", "")
        )
    )


def main():
    print("=============================================")
    print("        MONITOR GEMPA BMKG")
    print("=============================================")
    print("Polling data setiap 60 detik.")
    print("Tekan Ctrl+C untuk berhenti.")
    print("Sumber data: BMKG")
    print()

    gempa_terakhir = None

    while True:
        sekarang = waktu_sekarang()

        data = ambil_data()

        if data is None:
            print(f"[{sekarang}] Data tidak tersedia.")
        else:
            gempa = data.get("Infogempa", {}).get("gempa")

            if not gempa:
                print(f"[{sekarang}] Data gempa kosong.")
            else:
                identitas = identitas_gempa(gempa)

                if gempa_terakhir is None:
                    # Data pertama hanya dijadikan baseline.
                    gempa_terakhir = identitas
                    print(f"[{sekarang}] Data awal diterima.")
                    print(
                        f"Gempa terakhir BMKG: "
                        f"M{gempa.get('Magnitude', '-')}, "
                        f"{gempa.get('Wilayah', '-')}"
                    )

                elif identitas != gempa_terakhir:
                    tampilkan_gempa(gempa)
                    gempa_terakhir = identitas

                else:
                    print(f"[{sekarang}] Data tidak ada")

        print(f"Menunggu {INTERVAL} detik...")
        print()

        try:
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\nMonitor dihentikan.")
            break


if __name__ == "__main__":
    main()