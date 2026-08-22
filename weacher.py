import requests
import time
import os
from datetime import datetime

# ============================================================
# KONFIGURASI
# ============================================================

POLLING = 300  # 5 menit

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WIDTH = 45


# ============================================================
# WARNA
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"
WHITE = "\033[37m"


# ============================================================
# CLEAR
# ============================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ============================================================
# KONDISI CUACA
# ============================================================

WEATHER_LABELS = {
    0: "CERAH",
    1: "CERAH BERAWAN",
    2: "BERAWAN",
    3: "MENDUNG",

    45: "BERKABUT",
    48: "KABUT BEKU",

    51: "GERIMIS RINGAN",
    53: "GERIMIS",
    55: "GERIMIS LEBAT",

    61: "HUJAN RINGAN",
    63: "HUJAN",
    65: "HUJAN LEBAT",

    71: "SALJU RINGAN",
    73: "SALJU",
    75: "SALJU LEBAT",

    80: "HUJAN RINGAN",
    81: "HUJAN",
    82: "HUJAN SANGAT LEBAT",

    95: "BADAI PETIR",
    96: "BADAI PETIR + HUJAN ES",
    99: "BADAI PETIR + HUJAN ES LEBAT"
}


# ============================================================
# CARI LOKASI
# ============================================================

def cari_lokasi(nama_kota):

    params = {
        "name": nama_kota,
        "count": 1,
        "language": "id",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    return data["results"][0]


# ============================================================
# AMBIL DATA CUACA
# ============================================================

def ambil_cuaca(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation",
            "surface_pressure"
        ]),

        "hourly": ",".join([
            "temperature_2m",
            "weather_code",
            "precipitation_probability"
        ]),

        "forecast_hours": 6,
        "timezone": "auto",

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# TAMPILKAN CUACA
# ============================================================

def tampilkan_cuaca(data, lokasi):

    clear()

    current = data["current"]
    hourly = data["hourly"]

    suhu = current["temperature_2m"]
    kelembapan = current["relative_humidity_2m"]
    code = current["weather_code"]
    angin = current["wind_speed_10m"]
    arah_angin = current["wind_direction_10m"]
    hujan = current["precipitation"]
    tekanan = current["surface_pressure"]

    waktu_update = datetime.now().strftime(
        "%d %b %Y %H:%M:%S"
    )

    kondisi = WEATHER_LABELS.get(
        code,
        "[TIDAK DIKETAHUI]"
    )

    # ========================================================
    # HEADER
    # ========================================================

    print(CYAN + "=" * WIDTH + RESET)

    print(
        BOLD + CYAN +
        "             WEATHER MONITOR" +
        RESET
    )

    print(CYAN + "=" * WIDTH + RESET)

    print()

    # ========================================================
    # LOKASI
    # ========================================================

    print(
        f"{GREEN}Lokasi       :{RESET} "
        f"{lokasi['name']}"
    )

    if lokasi.get("country"):
        print(
            f"{GREEN}Negara       :{RESET} "
            f"{lokasi['country']}"
        )

    print(
        f"{GREEN}Update       :{RESET} "
        f"{waktu_update}"
    )

    print()

    # ========================================================
    # KONDISI SAAT INI
    # ========================================================

    print(
        f"{YELLOW}Suhu         :{RESET} "
        f"{suhu}°C"
    )

    print(
        f"{YELLOW}Kelembapan   :{RESET} "
        f"{kelembapan}%"
    )

    print(
        f"{YELLOW}Kondisi      :{RESET} "
        f"{kondisi}"
    )

    print(
        f"{YELLOW}Angin        :{RESET} "
        f"{angin} km/jam"
    )

    print(
        f"{YELLOW}Arah Angin   :{RESET} "
        f"{arah_angin}°"
    )

    print(
        f"{YELLOW}Hujan        :{RESET} "
        f"{hujan} mm"
    )

    print(
        f"{YELLOW}Tekanan      :{RESET} "
        f"{tekanan} hPa"
    )

    print()

    print(BLUE + "-" * WIDTH + RESET)

    print(BOLD + "Prakiraan:" + RESET)

    # ========================================================
    # PRAKIRAAN
    # ========================================================

    jumlah = min(
        6,
        len(hourly["time"])
    )

    for i in range(jumlah):

        waktu = hourly["time"][i]
        suhu_h = hourly["temperature_2m"][i]
        code_h = hourly["weather_code"][i]
        peluang = hourly["precipitation_probability"][i]

        jam = waktu[11:16]

        kondisi_h = WEATHER_LABELS.get(
            code_h,
            "[TIDAK DIKETAHUI]"
        )

        print(
            f"{jam}  "
            f"{kondisi_h:<18} "
            f"{suhu_h:>5.1f}°C  "
            f"{peluang:>2}%"
        )

    print(BLUE + "-" * WIDTH + RESET)

    print()

    print(
        GREEN +
        "[✓] Monitoring aktif..." +
        RESET
    )

    print(
        f"{CYAN}[i] Update berikutnya dalam "
        f"{POLLING // 60} menit.{RESET}"
    )


# ============================================================
# INPUT KOTA
# ============================================================

def input_kota():

    clear()

    print(CYAN + "=" * WIDTH + RESET)

    print(
        BOLD + CYAN +
        "             WEATHER MONITOR" +
        RESET
    )

    print(CYAN + "=" * WIDTH + RESET)

    print()

    print(
        YELLOW +
        "[!] Tekan X untuk keluar." +
        RESET
    )

    print()

    kota = input(
        f"{GREEN}Masukkan kota : {RESET}"
    ).strip()

    if kota.lower() == "x":
        return None

    return kota


# ============================================================
# MAIN
# ============================================================

def main():

    while True:

        kota = input_kota()

        # ====================================================
        # KELUAR
        # ====================================================

        if kota is None:

            clear()

            print(
                GREEN +
                "[✓] Program ditutup." +
                RESET
            )

            break

        # ====================================================
        # INPUT KOSONG
        # ====================================================

        if not kota:

            print()

            print(
                RED +
                "[!] Nama kota tidak boleh kosong." +
                RESET
            )

            time.sleep(2)

            continue

        # ====================================================
        # CARI LOKASI
        # ====================================================

        print()

        print(
            CYAN +
            "[...] Mencari lokasi..." +
            RESET
        )

        try:

            lokasi = cari_lokasi(kota)

        except requests.exceptions.RequestException as e:

            print()

            print(
                RED +
                "[!] Gagal menghubungi server." +
                RESET
            )

            print(
                f"{RED}[!] Error : {e}{RESET}"
            )

            time.sleep(3)

            continue

        # ====================================================
        # LOKASI TIDAK DITEMUKAN
        # ====================================================

        if lokasi is None:

            print()

            print(
                RED +
                "[!] Lokasi tidak ditemukan." +
                RESET
            )

            print(
                YELLOW +
                "[!] Silakan periksa nama kota." +
                RESET
            )

            time.sleep(3)

            continue

        # ====================================================
        # LOKASI DITEMUKAN
        # ====================================================

        latitude = lokasi["latitude"]
        longitude = lokasi["longitude"]

        print(
            GREEN +
            "[✓] Lokasi ditemukan." +
            RESET
        )

        print(
            f"{GREEN}[✓] Latitude  : "
            f"{latitude}{RESET}"
        )

        print(
            f"{GREEN}[✓] Longitude : "
            f"{longitude}{RESET}"
        )

        time.sleep(2)

        # ====================================================
        # MONITORING
        # ====================================================

        while True:

            try:

                data = ambil_cuaca(
                    latitude,
                    longitude
                )

                tampilkan_cuaca(
                    data,
                    lokasi
                )

                time.sleep(POLLING)

            except requests.exceptions.RequestException as e:

                print()

                print(
                    RED +
                    "[!] Gagal mengambil data cuaca." +
                    RESET
                )

                print(
                    f"{RED}[!] Error : {e}{RESET}"
                )

                print()

                print(
                    YELLOW +
                    "[...] Mencoba kembali dalam 30 detik..." +
                    RESET
                )

                time.sleep(30)

            except KeyboardInterrupt:

                # Kembali ke input kota
                break


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        clear()

        print(
            GREEN +
            "[✓] Program ditutup." +
            RESET
        )