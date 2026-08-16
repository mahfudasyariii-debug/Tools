import os
import sys
import time
import socket
import urllib.request
from colorama import init, Fore, Style

init(autoreset=True)

DOWNLOAD_URL = "https://speed.cloudflare.com/__down?bytes=25000000"
UPLOAD_URL = "https://speed.cloudflare.com/__up"


# =========================
# UI
# =========================

def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    input(
        f"\n{Fore.YELLOW}"
        "└─ Tekan Enter untuk kembali..."
        f"{Style.RESET_ALL}"
    )


def header(status="ONLINE", status_color=Fore.GREEN):
    print(
        f"{Fore.CYAN}  Network Test"
        f"{Style.RESET_ALL}"
    )

    print(
        f"{Fore.WHITE}  ─ Network Diagnostic Tool"
        f"{Style.RESET_ALL}"
    )

    print()

    print(
        f"{status_color}  ● {status}"
        f"{Style.RESET_ALL}"
    )

    print()


def progress_bar(label, current, total):
    width = 20

    if total <= 0:
        percent = 0
    else:
        percent = min(
            100,
            int((current / total) * 100)
        )

    filled = int(width * percent / 100)

    bar = (
        "█" * filled +
        "░" * (width - filled)
    )

    print(
        f"\r{Fore.CYAN}  {label:<12}"
        f"{Fore.GREEN}{bar}"
        f"{Fore.WHITE} {percent:3d}%",
        end="",
        flush=True
    )


# =========================
# NETWORK TEST
# =========================

def ping_test(host, count=5):
    times = []

    try:
        ip = socket.gethostbyname(host)

        for _ in range(count):
            start = time.perf_counter()

            sock = socket.create_connection(
                (ip, 443),
                timeout=3
            )

            sock.close()

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            times.append(elapsed)

        return sum(times) / len(times)

    except Exception:
        return None

<<<<<<< HEAD

def download_test():
=======
def download_test():
    MAX_TIME = 15

>>>>>>> af6b708 (update tools)
    start = time.perf_counter()
    received = 0

    request = urllib.request.Request(
        DOWNLOAD_URL,
        headers={
            "User-Agent": "NetworkTest/1.0"
        }
    )

<<<<<<< HEAD
    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        total = response.headers.get(
            "Content-Length"
        )

        if total:
            total = int(total)
        else:
            total = 25_000_000

        while True:
            chunk = response.read(
                64 * 1024
            )

            if not chunk:
                break

            received += len(chunk)

            progress_bar(
                "Download",
                received,
                total
            )
=======
    try:
        with urllib.request.urlopen(
            request,
            timeout=MAX_TIME + 5
        ) as response:

            total = response.headers.get(
                "Content-Length"
            )

            if total:
                total = int(total)
            else:
                total = 25_000_000

            while True:

                elapsed = (
                    time.perf_counter() - start
                )

                if elapsed >= MAX_TIME:
                    break

                chunk = response.read(
                    64 * 1024
                )

                if not chunk:
                    break

                received += len(chunk)

                progress_bar(
                    "Download",
                    received,
                    total
                )

    except Exception:
        pass
>>>>>>> af6b708 (update tools)

    elapsed = time.perf_counter() - start

    print()

<<<<<<< HEAD
    if elapsed <= 0:
=======
    if elapsed <= 0 or received <= 0:
>>>>>>> af6b708 (update tools)
        return 0

    return (
        received * 8
    ) / elapsed / 1_000_000


def upload_test():
<<<<<<< HEAD
=======
    MAX_TIME = 15

    data_size = 10_000_000_000
    chunk_size = 64 * 1024

    sent = 0
    start = time.perf_counter()

    class UploadStream:

        def read(self, size=-1):
            nonlocal sent

            elapsed = (
                time.perf_counter() - start
            )

            if elapsed >= MAX_TIME:
                return b""

            amount = min(
                chunk_size,
                data_size - sent
            )

            if amount <= 0:
                return b""

            chunk = b"0" * amount

            sent += amount

            progress_bar(
                "Upload",
                sent,
                data_size
            )

            return chunk

    stream = UploadStream()

    request = urllib.request.Request(
        UPLOAD_URL,
        data=stream,
        method="POST",
        headers={
            "Content-Type":
                "application/octet-stream",

            "Content-Length":
                str(data_size),

            "User-Agent":
                "NetworkTest/1.0"
        }
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=MAX_TIME + 5
        ) as response:

            response.read()

    except Exception:
        pass

    elapsed = (
        time.perf_counter() - start
    )

    print()

    if elapsed <= 0 or sent <= 0:
        return 0

    return (
        sent * 8
    ) / elapsed / 1_000_000


def upload_test():
>>>>>>> af6b708 (update tools)
    data_size = 10_000_000
    chunk_size = 64 * 1024

    sent = 0
    start = time.perf_counter()

    class UploadStream:

        def __init__(self):
            self.remaining = data_size

        def read(self, size=-1):
            nonlocal sent

            if self.remaining <= 0:
                return b""

            amount = min(
                chunk_size,
                self.remaining
            )

            chunk = b"0" * amount

            self.remaining -= amount
            sent += amount

            progress_bar(
                "Upload",
                sent,
                data_size
            )

            return chunk

    stream = UploadStream()

    request = urllib.request.Request(
        UPLOAD_URL,
        data=stream,
        method="POST",
        headers={
            "Content-Type":
                "application/octet-stream",

            "Content-Length":
                str(data_size),

            "User-Agent":
                "NetworkTest/1.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            response.read()

    except Exception:

        print()

        elapsed = (
            time.perf_counter() - start
        )

        if sent == 0 or elapsed <= 0:
            return None

        return (
            sent * 8
        ) / elapsed / 1_000_000

    elapsed = time.perf_counter() - start

    print()

    if elapsed <= 0:
        return 0

    return (
        sent * 8
    ) / elapsed / 1_000_000


# =========================
# QUALITY
# =========================

def kualitas_jaringan(
    ping,
    download,
    upload
):
    score = 0

    if ping <= 20:
        score += 3
    elif ping <= 50:
        score += 2
    elif ping <= 100:
        score += 1

    if download >= 50:
        score += 3
    elif download >= 20:
        score += 2
    elif download >= 5:
        score += 1

    if upload >= 20:
        score += 3
    elif upload >= 5:
        score += 2
    elif upload >= 1:
        score += 1

    if score >= 8:
        return "SANGAT BAIK", Fore.GREEN

    if score >= 5:
        return "BAIK", Fore.GREEN

    if score >= 3:
        return "CUKUP", Fore.YELLOW

    return "BURUK", Fore.RED


# =========================
# TEST MENU
# =========================

def network_test():

    clear()

    header(
        "TESTING",
        Fore.YELLOW
    )

    try:

        print(
            f"{Fore.WHITE}"
            "  Mengukur ping..."
            f"{Style.RESET_ALL}"
        )

        ping = ping_test(
            "speed.cloudflare.com"
        )

        if ping is None:
            raise RuntimeError(
                "Ping gagal."
            )

        progress_bar(
            "Ping",
            1,
            1
        )

        print()
        print()

        print(
            f"{Fore.WHITE}"
            "  Mengukur download..."
            f"{Style.RESET_ALL}"
        )

        download = download_test()

        print()

        print(
            f"{Fore.WHITE}"
            "  Mengukur upload..."
            f"{Style.RESET_ALL}"
        )

        upload = upload_test()

        if upload is None:
            raise RuntimeError(
                "Upload test gagal."
            )

        quality, color = (
            kualitas_jaringan(
                ping,
                download,
                upload
            )
        )

        clear()

        header(
            "COMPLETE",
            Fore.GREEN
        )

        print(
            f"  {Fore.WHITE}"
            f"Ping       : "
            f"{Fore.GREEN}"
            f"{ping:.2f} ms"
        )

        print(
            f"  {Fore.WHITE}"
            f"Download   : "
            f"{Fore.GREEN}"
            f"{download:.2f} Mbps"
        )

        print(
            f"  {Fore.WHITE}"
            f"Upload     : "
            f"{Fore.GREEN}"
            f"{upload:.2f} Mbps"
        )

        print()

        print(
            f"{Fore.CYAN}"
            "  Kualitas Jaringan"
            f"{Style.RESET_ALL}"
        )

        print()

        print(
            f"  {color}"
            f"{quality}"
            f"{Style.RESET_ALL}"
        )

        pause()

    except KeyboardInterrupt:

        clear()

        header(
            "CANCELLED",
            Fore.RED
        )

        pause()

    except Exception as error:

        clear()

        header(
            "ERROR",
            Fore.RED
        )

        print(
            f"  {Fore.RED}"
            f"{error}"
            f"{Style.RESET_ALL}"
        )

        pause()


# =========================
# MAIN MENU
# =========================

def main():

    while True:

        clear()

        header(
            "ONLINE",
            Fore.GREEN
        )

        print(
            f"{Fore.WHITE}"
            "  [1] "
            f"{Fore.GREEN}"
            "Tes Jaringan"
            f"{Style.RESET_ALL}"
        )

        print(
            f"{Fore.WHITE}"
            "  [2] "
            f"{Fore.RED}"
            "Keluar"
            f"{Style.RESET_ALL}"
        )

        print()

        choice = input(
            f"{Fore.CYAN}"
            "  └─ Pilih > "
            f"{Fore.WHITE}"
        ).strip()

        if choice == "1":

            network_test()

        elif choice == "2":

            clear()

            print(
                f"{Fore.GREEN}"
                "  ● Goodbye"
                f"{Style.RESET_ALL}"
            )

            sys.exit(0)

        else:

            print(
                f"\n{Fore.RED}"
                "  └─ Pilihan tidak valid."
                f"{Style.RESET_ALL}"
            )

            time.sleep(1)


if __name__ == "__main__":
    main()