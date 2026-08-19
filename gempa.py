import requests
import time
import os
from datetime import datetime, timedelta


# ============================================================
# KONFIGURASI
# ============================================================

URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

POLLING = 2

last_event = None

# Riwayat gempa selama tool berjalan
riwayat_gempa = []


# ============================================================
# WARNA TERMINAL
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
MAGENTA = "\033[95m"


# ============================================================
# SPINNER
# ============================================================

SPINNER = [
    "⠋",
    "⠙",
    "⠹",
    "⠸",
    "⠼",
    "⠴",
    "⠦",
    "⠧",
    "⠇",
    "⠏"
]

spinner_index = 0


# ============================================================
# CLEAR SCREEN
# ============================================================

def clear():

    os.system(
        "cls"
        if os.name == "nt"
        else "clear"
    )


# ============================================================
# STATUS MONITORING
# ============================================================

def status(teks):

    global spinner_index

    simbol = SPINNER[spinner_index]

    print(
        f"\r\033[K"
        f"{CYAN}{simbol}{RESET} "
        f"{GREEN}{teks}{RESET}",
        end="",
        flush=True
    )

    spinner_index = (
        spinner_index + 1
    ) % len(SPINNER)


# ============================================================
# WARNA MAGNITUDO
# ============================================================

def warna_magnitudo(magnitude):

    try:

        nilai = float(
            str(magnitude).replace(",", ".")
        )

        if nilai >= 7.0:

            return (
                f"{RED}{BOLD}"
                f"{magnitude}"
                f"{RESET}"
            )

        elif nilai >= 6.0:

            return (
                f"{RED}"
                f"{magnitude}"
                f"{RESET}"
            )

        elif nilai >= 4.0:

            return (
                f"{YELLOW}"
                f"{magnitude}"
                f"{RESET}"
            )

        else:

            return (
                f"{GREEN}"
                f"{magnitude}"
                f"{RESET}"
            )

    except Exception:

        return (
            f"{WHITE}"
            f"{magnitude}"
            f"{RESET}"
        )


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

        data = response.json()

        return data["Infogempa"]["gempa"]

    except Exception:

        return None


# ============================================================
# PROSES DATA GEMPA
# ============================================================

def proses_gempa(gempa):

    tanggal = gempa.get(
        "Tanggal",
        "-"
    )

    jam = gempa.get(
        "Jam",
        "-"
    )


    # ========================================================
    # KONVERSI WIB -> WITA
    # ========================================================

    try:

        dt_wib = datetime.strptime(
            f"{tanggal} {jam}",
            "%d %b %Y %H:%M:%S"
        )

        dt_wita = (
            dt_wib +
            timedelta(hours=1)
        )

        waktu_bmkg = (
            dt_wita.strftime(
                "%d %b %Y %H:%M:%S"
            )
            + " WITA"
        )

    except Exception:

        dt_wita = None

        waktu_bmkg = (
            f"{tanggal} {jam}"
        )


    # ========================================================
    # WAKTU TERDETEKSI
    # ========================================================

    waktu_terdeteksi = datetime.now()


    # ========================================================
    # HITUNG DELAY
    # ========================================================

    if dt_wita:

        delay = (
            waktu_terdeteksi -
            dt_wita
        )

        delay_text = (
            str(delay)
            .split(".")[0]
        )

    else:

        delay_text = "Tidak diketahui"


    # ========================================================
    # BUAT DATA RIWAYAT
    # ========================================================

    data_riwayat = {

        "waktu_bmkg": waktu_bmkg,

        "waktu_terdeteksi":
            waktu_terdeteksi.strftime(
                "%d %b %Y %H:%M:%S"
            ) + " WITA",

        "delay": delay_text,

        "magnitudo":
            gempa.get(
                "Magnitude",
                "-"
            ),

        "kedalaman":
            gempa.get(
                "Kedalaman",
                "-"
            ),

        "koordinat":
            gempa.get(
                "Coordinates",
                "-"
            ),

        "wilayah":
            gempa.get(
                "Wilayah",
                "-"
            ),

        "potensi":
            gempa.get(
                "Potensi",
                "-"
            ),

        "dirasakan":
            gempa.get(
                "Dirasakan",
                "-"
            )
    }

    return data_riwayat


# ============================================================
# TAMPILKAN DETAIL GEMPA
# ============================================================

def tampilkan_gempa(gempa):

    data = proses_gempa(gempa)

    # Simpan ke riwayat
    riwayat_gempa.append(data)


    # ========================================================
    # HAPUS STATUS MONITORING
    # ========================================================

    print("\r\033[K")


    # ========================================================
    # HEADER
    # ========================================================

    print(
        f"{RED}"
        "============================================="
        f"{RESET}"
    )

    print(
        f"{RED}{BOLD}"
        "          ⚠ GEMPA TERDETEKSI"
        f"{RESET}"
    )

    print(
        f"{RED}"
        "============================================="
        f"{RESET}"
    )

    print()


    # ========================================================
    # WAKTU
    # ========================================================

    print(
        f"{YELLOW}Waktu BMKG :{RESET} "
        f"{data['waktu_bmkg']}"
    )

    print(
        f"{YELLOW}Terdeteksi :{RESET} "
        f"{data['waktu_terdeteksi']}"
    )

    print(
        f"{YELLOW}Delay      :{RESET} "
        f"{data['delay']}"
    )

    print()


    # ========================================================
    # DATA GEMPA
    # ========================================================

    print(
        f"{RED}Magnitudo  :{RESET} "
        f"{warna_magnitudo(data['magnitudo'])}"
    )

    print(
        f"{CYAN}Kedalaman  :{RESET} "
        f"{data['kedalaman']}"
    )

    print(
        f"{CYAN}Koordinat  :{RESET} "
        f"{data['koordinat']}"
    )

    print(
        f"{WHITE}Wilayah    :{RESET} "
        f"{data['wilayah']}"
    )

    print(
        f"{YELLOW}Potensi    :{RESET} "
        f"{data['potensi']}"
    )

    print(
        f"{MAGENTA}Dirasakan  :{RESET} "
        f"{data['dirasakan']}"
    )

    print()


    # ========================================================
    # FOOTER
    # ========================================================

    print(
        f"{GRAY}"
        "============================================="
        f"{RESET}"
    )

    print(
        f"{GREEN}Sumber data:{RESET} BMKG"
    )

    print(
        f"{GRAY}"
        "============================================="
        f"{RESET}"
    )

    print()


# ============================================================
# TAMPILKAN RIWAYAT
# ============================================================

def tampilkan_riwayat():

    clear()

    print(
        f"{CYAN}"
        "============================================="
        f"{RESET}"
    )

    print(
        f"{CYAN}{BOLD}"
        "          RIWAYAT MONITOR GEMPA"
        f"{RESET}"
    )

    print(
        f"{CYAN}"
        "============================================="
        f"{RESET}"
    )

    print()


    # ========================================================
    # BELUM ADA RIWAYAT
    # ========================================================

    if not riwayat_gempa:

        print(
            f"{YELLOW}"
            "Belum ada gempa yang terdeteksi."
            f"{RESET}"
        )

        print()

        input(
            "Tekan Enter untuk kembali..."
        )

        return


    # ========================================================
    # JUMLAH GEMPA
    # ========================================================

    print(
        f"{GREEN}"
        f"Total gempa terdeteksi: "
        f"{len(riwayat_gempa)}"
        f"{RESET}"
    )

    print()


    # ========================================================
    # TAMPILKAN SEMUA RIWAYAT
    # ========================================================

    for nomor, data in enumerate(
        riwayat_gempa,
        start=1
    ):

        print(
            f"{GRAY}"
            "============================================="
            f"{RESET}"
        )

        print(
            f"{WHITE}{BOLD}"
            f"Gempa #{nomor}"
            f"{RESET}"
        )

        print()

        print(
            f"{YELLOW}Waktu BMKG :{RESET} "
            f"{data['waktu_bmkg']}"
        )

        print(
            f"{YELLOW}Terdeteksi :{RESET} "
            f"{data['waktu_terdeteksi']}"
        )

        print(
            f"{YELLOW}Delay      :{RESET} "
            f"{data['delay']}"
        )

        print(
            f"{RED}Magnitudo  :{RESET} "
            f"{warna_magnitudo(data['magnitudo'])}"
        )

        print(
            f"{CYAN}Kedalaman  :{RESET} "
            f"{data['kedalaman']}"
        )

        print(
            f"{CYAN}Koordinat  :{RESET} "
            f"{data['koordinat']}"
        )

        print(
            f"{WHITE}Wilayah    :{RESET} "
            f"{data['wilayah']}"
        )

        print(
            f"{YELLOW}Potensi    :{RESET} "
            f"{data['potensi']}"
        )

        print(
            f"{MAGENTA}Dirasakan  :{RESET} "
            f"{data['dirasakan']}"
        )

        print()


    print(
        f"{GRAY}"
        "============================================="
        f"{RESET}"
    )

    print()

    input(
        "Tekan Enter untuk kembali..."
    )


# ============================================================
# MONITOR GEMPA
# ============================================================

def monitor_gempa():

    global last_event

    clear()


    # ========================================================
    # HEADER
    # ========================================================

    print(
        f"{CYAN}"
        "============================================="
        f"{RESET}"
    )

    print(
        f"{CYAN}{BOLD}"
        "       MONITOR GEMPA BMKG - REALTIME"
        f"{RESET}"
    )

    print(
        f"{CYAN}"
        "============================================="
        f"{RESET}"
    )

    print()

    print(
        f"{GREEN}Status :{RESET} "
        f"{WHITE}TERHUBUNG{RESET}"
    )

    print(
        f"{CYAN}Feed   :{RESET} "
        f"{WHITE}BMKG{RESET}"
    )

    print(
        f"{YELLOW}Polling:{RESET} "
        f"{WHITE}{POLLING} detik{RESET}"
    )

    print()

    print(
        f"{GRAY}"
        "Menunggu gempa baru..."
        f"{RESET}"
    )

    print()


    # ========================================================
    # DATA AWAL
    # ========================================================

    gempa_awal = ambil_gempa()


    if gempa_awal:

        last_event = (
            gempa_awal.get("Tanggal"),
            gempa_awal.get("Jam"),
            gempa_awal.get("Magnitude"),
            gempa_awal.get("Coordinates")
        )


    print()


    # ========================================================
    # MONITORING
    # ========================================================

    try:

        while True:

            gempa = ambil_gempa()


            if gempa:

                event_id = (
                    gempa.get("Tanggal"),
                    gempa.get("Jam"),
                    gempa.get("Magnitude"),
                    gempa.get("Coordinates")
                )


                # ============================================
                # GEMPA BARU
                # ============================================

                if event_id != last_event:

                    tampilkan_gempa(
                        gempa
                    )

                    last_event = event_id


            status(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                "Monitoring..."
            )

            time.sleep(POLLING)


    # ========================================================
    # KEMBALI KE MENU
    # ========================================================

    except KeyboardInterrupt:

        print()
        print()

        print(
            f"{YELLOW}"
            "Monitoring dihentikan."
            f"{RESET}"
        )

        time.sleep(1)


# ============================================================
# MENU UTAMA
# ============================================================

def menu_utama():

    while True:

        clear()

        print(
            f"{CYAN}"
            "============================================="
            f"{RESET}"
        )

        print(
            f"{CYAN}{BOLD}"
            "          MONITOR GEMPA BMKG"
            f"{RESET}"
        )

        print(
            f"{CYAN}"
            "============================================="
            f"{RESET}"
        )

        print()

        print(
            f"{WHITE}1.{RESET} "
            f"Monitor gempa"
        )

        print(
            f"{WHITE}2.{RESET} "
            f"Riwayat hasil monitor "
            f"{GRAY}({len(riwayat_gempa)} gempa){RESET}"
        )

        print(
            f"{WHITE}0.{RESET} "
            f"Keluar"
        )

        print()

        pilihan = input(
            "Pilih : "
        ).strip()


        # ====================================================
        # MONITOR
        # ====================================================

        if pilihan == "1":

            monitor_gempa()


        # ====================================================
        # RIWAYAT
        # ====================================================

        elif pilihan == "2":

            tampilkan_riwayat()


        # ====================================================
        # KELUAR
        # ====================================================

        elif pilihan == "0":

            clear()

            print(
                f"{GREEN}"
                "Program dihentikan."
                f"{RESET}"
            )

            break


        # ====================================================
        # PILIHAN SALAH
        # ====================================================

        else:

            print()

            print(
                f"{RED}"
                "Pilihan tidak valid!"
                f"{RESET}"
            )

            time.sleep(1)


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    menu_utama()