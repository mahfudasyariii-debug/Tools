import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# ===============
# ENGINEERING
# ===============

def version():
    return "5.0.0"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def error():
    print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")


# ===============
# DOWNLOAD
# ===============

def download_video():
    while True:
        url = input("URL Video > ")

        result = subprocess.run([
            "yt-dlp",
            "-f", "bv*+ba/b",
            "--merge-output-format",
            "mp4",
            url
        ])

        if result.returncode == 0:
            print(f"\n{Fore.GREEN}Download berhasil!{Style.RESET_ALL}")
            input("\nEnter untuk kembali ke menu...")
            break

        print(f"\n{Fore.RED}Gagal download! URL mungkin salah.{Style.RESET_ALL}")
        print("[R] Try Again")
        print("[M] Back to Menu")

        pilihan = input("> ").lower()

        if pilihan == "r":
            clear()
            continue

        elif pilihan == "m":
            break

        else:
            print("Pilihan tidak valid.")


def download_audio():
    url = input("URL Audio > ")

    subprocess.run([
        "yt-dlp",
        "-x",
        url
    ])


def download_mp3():
    url = input("URL Audio MP3 > ")

    subprocess.run([
        "yt-dlp",
        "-x",
        "--audio-format",
        "mp3",
        url
    ])


# ===============
# MENU
# ===============

def tampilan(daftar):
    for nomor, nama in daftar.items():
        print(f"{Fore.RED}{nomor}.{Style.RESET_ALL} {nama}")


def menu():
    clear()

    print(f"\n   --Version: {version()}")

    print(f"""
    
         {Fore.LIGHTBLUE_EX}TOOL DOWNLOAD MP4/MP3{Style.RESET_ALL}
    ---------------------------------
            {Fore.YELLOW}===== MENU ====={Style.RESET_ALL}
    """)

    daftar = {
        "1": "download video",
        "2": "download audio",
        "3": "download mp3",
        "4": "keluar",
    }

    tampilan(daftar)


# ===============
# ACTION
# ===============

aksi = {
    "1": download_video,
    "2": download_audio,
    "3": download_mp3,
}


# ===============
# MAIN LOOP
# ===============

while True:
    menu()

    pilih = input(
        f"\n    {Fore.LIGHTRED_EX}Pilih nomor : {Style.RESET_ALL}"
    )

    if pilih == "4":
        clear()
        break

    fungsi = aksi.get(pilih)

    if fungsi:
        fungsi()
    else:
        error()