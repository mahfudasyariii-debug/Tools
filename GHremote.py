from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import tempfile
import os
import json


# ═════════════════════════════════════
# GHremote
# Git Operation Lab
# ═════════════════════════════════════

APP_NAME = "ghremote"

ANDROID_STORAGE = Path("/storage/emulated/0")
LINUX_STORAGE = Path.home()
HISTORY_FILE = Path.home() / ".ghremote_history.log"


# ═════════════════════════════════════
# COLORS
# ═════════════════════════════════════

RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
WHITE = "\033[37m"
DIM = "\033[2m"


def color(text, code):
    return f"{code}{text}{RESET}"


# ═════════════════════════════════════
# TRANSLATION
# ═════════════════════════════════════

TEXT = {
    "id": {
        "language": "bahasa",
        "device": "perangkat",
        "platform": "platform",
        "indonesia": "indonesia",
        "english": "inggris",
        "android": "android (termux)",
        "linux": "linux",
        "upload": "unggah",
        "update": "update",
        "delete": "hapus",
        "history": "riwayat",
        "status": "status repositori",
        "back": "kembali",
        "exit": "keluar",
        "cancel": "batal",
        "file": "file",
        "repository": "repository",
        "filename_empty": "nama file kosong.",
        "invalid_choice": "pilihan tidak valid.",
        "upload_test": "Unggah",
        "update_test": "Update",
        "delete_test": "Hapus",
        "select_file": "Pilih file",
        "current_folder": "folder saat ini",
        "parent": "naik satu folder",
        "empty_folder": "folder ini kosong.",
        "folder_error": "gagal membaca folder:",
        "file_selected": "file dipilih:",
        "copying_file": "menyalin file ke repository...",
        "copy_failed": "gagal menyalin file:",
        "select_repository": "pilih repository GitHub",
        "loading_repositories": "memuat repository...",
        "no_repositories": "tidak ada repository yang ditemukan.",
        "repository_error": "gagal mengambil repository:",
        "repository_selected": "repository dipilih:",
        "github_required": "GitHub CLI (gh) tidak ditemukan.",
        "github_login_required": "silakan login ke GitHub CLI terlebih dahulu.",
        "cloning": "mengambil repository...",
        "clone_failed": "gagal mengambil repository:",
        "adding_file": "menambahkan file...",
        "removing_file": "menghapus file...",
        "creating_commit": "membuat commit...",
        "sending_github": "mengirim perubahan ke GitHub...",
        "commit_failed": "commit gagal.",
        "push_failed": "push gagal.",
        "upload_success": "unggah berhasil.",
        "update_success": "update berhasil.",
        "delete_success": "penghapusan berhasil.",
        "file_exists": "file sudah ada di repository.",
        "file_not_found": "file tidak ditemukan di repository.",
        "select_target_file": "pilih file target di repository",
        "replacing_file": "mengganti file lama dengan file baru...",
        "no_files": "tidak ada file yang dapat dipilih.",
        "no_history": "belum ada riwayat operasi.",
        "history_read_failed": "gagal membaca riwayat:",
        "history_save_failed": "gagal menyimpan riwayat:",
        "repository_status": "status repository",
        "operation_failed": "operasi gagal.",
        "operation_success": "operasi berhasil.",
        "continue": "tekan ENTER untuk melanjutkan",
        "closed": "GHremote ditutup.",
        "workspace": "workspace sementara",
        "menu": "menu utama",
        "select_language": "pilih bahasa",
        "select_device": "pilih perangkat",
        "change_language": "ubah bahasa",
        "change_device": "ubah perangkat",
        "language_saved": "bahasa dipilih:",
        "device_saved": "perangkat dipilih:",
        "no_changes": "tidak ada perubahan untuk diproses.",
        "repo_status_failed": "gagal membaca status repository:",
        "repo_clean": "repository bersih, tidak ada perubahan.",
        "repo_changes": "perubahan terdeteksi.",
        "configuring_identity": "mengatur identitas commit...",
    },
    "en": {
        "language": "language",
        "device": "device",
        "platform": "platform",
        "indonesia": "indonesian",
        "english": "english",
        "android": "android (termux)",
        "linux": "linux",
        "upload": "upload",
        "update": "update",
        "delete": "delete",
        "history": "history",
        "status": "repository status",
        "back": "back",
        "exit": "exit",
        "cancel": "cancel",
        "file": "file",
        "repository": "repository",
        "filename_empty": "filename is empty.",
        "invalid_choice": "invalid choice.",
        "upload_test": "upload",
        "update_test": "update",
        "delete_test": "delete",
        "select_file": "select file",
        "current_folder": "current folder",
        "parent": "go to parent folder",
        "empty_folder": "this folder is empty.",
        "folder_error": "failed to read folder:",
        "file_selected": "selected file:",
        "copying_file": "copying file to repository...",
        "copy_failed": "failed to copy file:",
        "select_repository": "select GitHub repository",
        "loading_repositories": "loading repositories...",
        "no_repositories": "no repositories found.",
        "repository_error": "failed to get repositories:",
        "repository_selected": "selected repository:",
        "github_required": "GitHub CLI (gh) was not found.",
        "github_login_required": "please login to GitHub CLI first.",
        "cloning": "getting repository...",
        "clone_failed": "failed to get repository:",
        "adding_file": "adding file...",
        "removing_file": "removing file...",
        "creating_commit": "creating commit...",
        "sending_github": "sending changes to GitHub...",
        "commit_failed": "commit failed.",
        "push_failed": "push failed.",
        "upload_success": "upload successful.",
        "update_success": "update successful.",
        "delete_success": "delete successful.",
        "file_exists": "file already exists in repository.",
        "file_not_found": "file not found in repository.",
        "select_target_file": "select target file in repository",
        "replacing_file": "replacing old file with new file...",
        "no_files": "no selectable files.",
        "no_history": "no operation history.",
        "history_read_failed": "failed to read history:",
        "history_save_failed": "failed to save history:",
        "repository_status": "repository status",
        "operation_failed": "operation failed.",
        "operation_success": "operation successful.",
        "continue": "press ENTER to continue",
        "closed": "GHremote closed.",
        "workspace": "temporary workspace",
        "menu": "main menu",
        "select_language": "select language",
        "select_device": "select device",
        "change_language": "change language",
        "change_device": "change device",
        "language_saved": "selected language:",
        "device_saved": "selected device:",
        "no_changes": "there are no changes to process.",
        "repo_status_failed": "failed to read repository status:",
        "repo_clean": "repository is clean, no changes.",
        "repo_changes": "changes detected.",
        "configuring_identity": "configuring commit identity...",
    },
}


def t(language, key):
    return TEXT.get(language, TEXT["id"]).get(key, key)


# ═════════════════════════════════════
# TERMINAL
# ═════════════════════════════════════

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def pause(language):
    input(
        f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} "
        f"{color(t(language, 'continue'), DIM)}"
    )


def header(title):
    print(color(APP_NAME, CYAN))
    print(color(f"{APP_NAME} / {title}", DIM))
    print()


# ═════════════════════════════════════
# COMMAND
# ═════════════════════════════════════

def run_command(*args):
    try:
        return subprocess.run(
            args,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    except Exception as error:
        print(f"\n{color('error:', RED)} {error}")
        return None


# ═════════════════════════════════════
# GIT
# ═════════════════════════════════════

def run_git(repo, *args, show_command=True):
    command = ["git", "-C", str(repo), *args]

    if show_command:
        print()
        print(color("$", CYAN), color(" ".join(command), WHITE))

    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        print(f"\n{color('git:', RED)} Git executable not found.")
        return None
    except Exception as error:
        print(f"\n{color('git:', RED)} {error}")
        return None

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    return result


# ═════════════════════════════════════
# HISTORY
# ═════════════════════════════════════

def save_history(action, filename, status, repository=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repo = repository or "-"
    entry = (
        f"[{timestamp}] {action.upper():<6} | "
        f"{status.upper():<7} | {filename} | {repo}\n"
    )

    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(entry)
    except Exception as error:
        print(
            f"\n{color('warning:', YELLOW)} "
            f"{t('id', 'history_save_failed')} {error}"
        )


def show_history(language):
    clear_screen()
    header(t(language, "history"))

    if not HISTORY_FILE.exists():
        print(color(t(language, "no_history"), DIM))
        pause(language)
        return

    try:
        history = HISTORY_FILE.read_text(encoding="utf-8").strip()
        print(history if history else color(t(language, "no_history"), DIM))
    except Exception as error:
        print(
            f"\n{color('error:', RED)} "
            f"{t(language, 'history_read_failed')} {error}"
        )
    pause(language)


# ═════════════════════════════════════
# STORAGE ROOT
# ═════════════════════════════════════

def get_storage_root(platform):
    if platform == "termux":
        if ANDROID_STORAGE.exists():
            return ANDROID_STORAGE
        return Path.home()
    return LINUX_STORAGE


# ═════════════════════════════════════
# FILE PICKER
# ═════════════════════════════════════

def choose_file(language, platform):
    current = get_storage_root(platform)
    root = current

    while True:
        clear_screen()
        header(t(language, "select_file"))
        print(color(f"{t(language, 'current_folder')}: ", DIM))
        print(color(str(current), CYAN))
        print()

        try:
            items = sorted(
                current.iterdir(),
                key=lambda item: (item.is_file(), item.name.lower()),
            )
        except Exception as error:
            print(
                f"{color('error:', RED)} "
                f"{t(language, 'folder_error')} {error}"
            )
            pause(language)
            return None

        if not items:
            print(color(t(language, "empty_folder"), DIM))

        for number, item in enumerate(items, 1):
            if item.is_dir():
                label = f"📁 {item.name}/"
                print(f"{color(f'[{number}]', YELLOW)} {color(label, CYAN)}")
            else:
                print(
                    f"{color(f'[{number}]', YELLOW)} "
                    f"{color(item.name, WHITE)}"
                )

        print()
        if current != root:
            print(f"{color('[..]', YELLOW)} {t(language, 'parent')}")
        print(f"{color('[0]', RED)} {t(language, 'cancel')}")

        choice = input(
            f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} "
        ).strip()

        if choice == "0":
            return None
        if choice == "..":
            if current != root:
                current = current.parent
            continue
        if not choice.isdigit():
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            pause(language)
            continue

        index = int(choice) - 1
        if not 0 <= index < len(items):
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            pause(language)
            continue

        selected = items[index]
        if selected.is_dir():
            current = selected
            continue
        return selected


# ═════════════════════════════════════
# GITHUB
# ═════════════════════════════════════

def get_github_repositories(language):
    result = run_command(
        "gh", "repo", "list",
        "--json", "nameWithOwner,isArchived",
        "--limit", "100",
    )

    if result is None:
        print(f"\n{color(t(language, 'github_required'), RED)}")
        return []

    if result.returncode != 0:
        error = result.stderr.strip()
        lower = error.lower()
        if "not logged" in lower or "auth login" in lower or "authentication" in lower:
            print(f"\n{color(t(language, 'github_login_required'), RED)}")
        else:
            print(
                f"\n{color('error:', RED)} "
                f"{t(language, 'repository_error')} {error}"
            )
        return []

    try:
        repositories = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as error:
        print(f"\n{color('error:', RED)} {error}")
        return []

    return [
        repo.get("nameWithOwner", "")
        for repo in repositories
        if repo.get("nameWithOwner") and not repo.get("isArchived", False)
    ]


def choose_github_repository(language):
    clear_screen()
    header(t(language, "select_repository"))
    print(color(t(language, "loading_repositories"), DIM))

    repositories = get_github_repositories(language)
    if not repositories:
        print(color(t(language, "no_repositories"), DIM))
        pause(language)
        return None

    print()
    for number, repository in enumerate(repositories, 1):
        print(
            f"{color(f'[{number}]', YELLOW)} "
            f"{color(repository, WHITE)}"
        )

    print(f"\n{color('[0]', RED)} {t(language, 'cancel')}")

    while True:
        choice = input(
            f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} "
        ).strip()
        if choice == "0":
            return None
        if not choice.isdigit():
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            continue

        index = int(choice) - 1
        if not 0 <= index < len(repositories):
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            continue

        selected = repositories[index]
        print(f"\n{color(t(language, 'repository_selected'), DIM)}")
        print(color(selected, CYAN))
        return selected


# ═════════════════════════════════════
# CLONE
# ═════════════════════════════════════

def clone_repository(repository, workspace, language):
    print(f"\n{color(t(language, 'cloning'), DIM)}")

    result = run_command("gh", "repo", "clone", repository, str(workspace))
    if result is None:
        print(f"\n{color(t(language, 'github_required'), RED)}")
        return False

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

    if result.returncode != 0:
        print(f"\n{color(t(language, 'clone_failed'), RED)}")
        return False

    return True


# ═════════════════════════════════════
# REPOSITORY FILE PICKER
# ═════════════════════════════════════

def choose_repo_file(language, repo):
    files = sorted(
        [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts],
        key=lambda p: str(p).lower(),
    )

    if not files:
        print(f"\n{color(t(language, 'no_files'), DIM)}")
        return None

    print()
    header(t(language, "delete_test"))

    for number, path in enumerate(files, 1):
        rel = path.relative_to(repo)
        print(f"{color(f'[{number}]', YELLOW)} {color(str(rel), WHITE)}")

    print(f"\n{color('[0]', RED)} {t(language, 'cancel')}")

    while True:
        choice = input(
            f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} "
        ).strip()
        if choice == "0":
            return None
        if not choice.isdigit():
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            continue

        index = int(choice) - 1
        if not 0 <= index < len(files):
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            continue
        return files[index]


# ═════════════════════════════════════
# GITHUB COMMIT IDENTITY
# ═════════════════════════════════════

def get_github_user(language):
    """
    Get the currently authenticated GitHub username using gh.
    """
    result = run_command("gh", "api", "user", "--jq", ".login")

    if result is None:
        print(f"\n{color(t(language, 'github_required'), RED)}")
        return None

    if result.returncode != 0:
        error = result.stderr.strip()
        print(
            f"\n{color('error:', RED)} "
            f"{error or t(language, 'github_login_required')}"
        )
        return None

    username = result.stdout.strip()

    if not username:
        print(
            f"\n{color('error:', RED)} "
            f"{t(language, 'github_login_required')}"
        )
        return None

    return username


def configure_commit_identity(repo, language):
    """
    Configure the temporary clone to use GitHub's noreply email.
    This avoids GitHub GH007 email privacy rejection.
    """
    username = get_github_user(language)

    if not username:
        return False

    # GitHub's privacy-safe noreply format.
    noreply_email = f"{username}@users.noreply.github.com"

    name_result = run_git(
        repo,
        "config",
        "user.name",
        username,
        show_command=False,
    )

    if name_result is None or name_result.returncode != 0:
        print(
            f"\n{color('error:', RED)} "
            f"failed to configure git user.name"
        )
        return False

    email_result = run_git(
        repo,
        "config",
        "user.email",
        noreply_email,
        show_command=False,
    )

    if email_result is None or email_result.returncode != 0:
        print(
            f"\n{color('error:', RED)} "
            f"failed to configure git user.email"
        )
        return False

    return True


# ═════════════════════════════════════
# COMMIT + PUSH
# ═════════════════════════════════════

def commit_and_push(repo, filename, action, language, repository):
    print(
        f"\n{color(t(language, 'configuring_identity'), DIM)}"
    )

    # Configure a GitHub-safe commit identity in the temporary clone.
    if not configure_commit_identity(repo, language):
        save_history(action, filename, "FAILED", repository)
        return False

    add = run_git(repo, "add", "-A")
    if add is None or add.returncode != 0:
        print(f"\n{color(t(language, 'operation_failed'), RED)}")
        save_history(action, filename, "FAILED", repository)
        return False

    diff = run_git(repo, "diff", "--cached", "--quiet", show_command=False)
    if diff is not None and diff.returncode == 0:
        print(f"\n{color(t(language, 'no_changes'), YELLOW)}")
        save_history(action, filename, "FAILED", repository)
        return False

    print(f"\n{color(t(language, 'creating_commit'), DIM)}")
    commit = run_git(repo, "commit", "-m", f"{action} {filename}")
    if commit is None or commit.returncode != 0:
        print(f"\n{color(t(language, 'commit_failed'), RED)}")
        save_history(action, filename, "FAILED", repository)
        return False

    print(color(t(language, "sending_github"), DIM))
    push = run_git(repo, "push")
    if push is None or push.returncode != 0:
        print(f"\n{color(t(language, 'push_failed'), RED)}")
        save_history(action, filename, "FAILED", repository)
        return False

    save_history(action, filename, "SUCCESS", repository)
    if action == "Upload":
        message = "upload_success"
    elif action == "Update":
        message = "update_success"
    else:
        message = "delete_success"
    print(f"\n{color(t(language, message), GREEN)}")
    return True


# ═════════════════════════════════════
# UPLOAD
# ═════════════════════════════════════

def upload_test(language, platform):
    selected_file = choose_file(language, platform)
    if selected_file is None:
        return

    repository = choose_github_repository(language)
    if repository is None:
        return

    clear_screen()
    header(t(language, "upload_test"))
    print(f"{color(t(language, 'file_selected'), DIM)} {color(str(selected_file), CYAN)}")
    print(f"{color(t(language, 'repository_selected'), DIM)} {color(repository, CYAN)}")

    try:
        with tempfile.TemporaryDirectory(prefix="ghremote_") as temp:
            workspace = Path(temp) / "repo"
            print(f"\n{color(t(language, 'workspace'), DIM)}")
            print(color(str(workspace), DIM))

            if not clone_repository(repository, workspace, language):
                save_history("Upload", selected_file.name, "FAILED", repository)
                pause(language)
                return

            destination = workspace / selected_file.name
            if destination.exists():
                print(f"\n{color(t(language, 'file_exists'), YELLOW)}")
                save_history("Upload", selected_file.name, "FAILED", repository)
                pause(language)
                return

            print(f"\n{color(t(language, 'copying_file'), DIM)}")
            try:
                shutil.copy2(selected_file, destination)
            except Exception as error:
                print(f"\n{color(t(language, 'copy_failed'), RED)} {error}")
                save_history("Upload", selected_file.name, "FAILED", repository)
                pause(language)
                return

            commit_and_push(
                workspace,
                selected_file.name,
                "Upload",
                language,
                repository,
            )

    except Exception as error:
        print(f"\n{color('error:', RED)} {error}")
        save_history("Upload", selected_file.name, "FAILED", repository)

    pause(language)


# ═════════════════════════════════════
# UPDATE
# ═════════════════════════════════════

def get_github_file_info(repository, file_path, language):
    """
    Get file metadata from GitHub without cloning the repository.
    """
    endpoint = f"repos/{repository}/contents/{file_path}"

    result = run_command(
        "gh",
        "api",
        endpoint,
    )

    if result is None:
        print(f"\n{color(t(language, 'github_required'), RED)}")
        return None

    if result.returncode != 0:
        error = result.stderr.strip()
        print(
            f"\n{color('error:', RED)} "
            f"{error or t(language, 'file_not_found')}"
        )
        return None

    try:
        return json.loads(result.stdout or "{}")
    except json.JSONDecodeError as error:
        print(f"\n{color('error:', RED)} {error}")
        return None


def get_repository_tree(repository, language):
    """
    Get repository file paths through GitHub's recursive tree API.
    No clone is performed.
    """
    try:
        repo_info = run_command(
            "gh",
            "api",
            f"repos/{repository}",
        )

        if repo_info is None or repo_info.returncode != 0:
            return []

        data = json.loads(repo_info.stdout or "{}")
        branch = data.get("default_branch", "main")

        branch_info = run_command(
            "gh",
            "api",
            f"repos/{repository}/git/ref/heads/{branch}",
        )

        if branch_info is None or branch_info.returncode != 0:
            return []

        branch_data = json.loads(branch_info.stdout or "{}")
        sha = branch_data.get("object", {}).get("sha")

        if not sha:
            return []

        tree_result = run_command(
            "gh",
            "api",
            f"repos/{repository}/git/trees/{sha}?recursive=1",
        )

        if tree_result is None or tree_result.returncode != 0:
            return []

        tree_data = json.loads(tree_result.stdout or "{}")

        return sorted(
            [
                item["path"]
                for item in tree_data.get("tree", [])
                if item.get("type") == "blob"
            ],
            key=str.lower,
        )

    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def choose_remote_file(language, repository):
    """
    Show files in the selected GitHub repository and return a target path.
    """
    clear_screen()
    header(t(language, "select_target_file"))

    print(
        color(
            t(language, "fetching_file"),
            DIM
        )
    )

    files = get_repository_tree(
        repository,
        language
    )

    if not files:
        print(
            f"\n{color(t(language, 'no_files'), DIM)}"
        )
        pause(language)
        return None

    print()

    for number, file_path in enumerate(files, 1):
        print(
            f"{color(f'[{number}]', YELLOW)} "
            f"{color(file_path, WHITE)}"
        )

    print()
    print(
        f"{color('[0]', RED)} "
        f"{t(language, 'cancel')}"
    )

    while True:
        choice = input(
            f"\n{color(APP_NAME, CYAN)} "
            f"{color('>', GREEN)} "
        ).strip()

        if choice == "0":
            return None

        if not choice.isdigit():
            print(
                f"\n{color(t(language, 'invalid_choice'), RED)}"
            )
            continue

        index = int(choice) - 1

        if not 0 <= index < len(files):
            print(
                f"\n{color(t(language, 'invalid_choice'), RED)}"
            )
            continue

        return files[index]


def update_file_via_github_api(
    selected_file,
    repository,
    target_path,
    language,
):
    """
    Replace an existing GitHub file directly through the Contents API.

    The local file is uploaded as base64 through `gh api`.
    GitHub creates the commit and updates the target file.
    """
    info = get_github_file_info(
        repository,
        target_path,
        language
    )

    if not info:
        return False

    sha = info.get("sha")

    if not sha:
        print(
            f"\n{color('error:', RED)} "
            f"{t(language, 'file_not_found')}"
        )
        return False

    try:
        import base64

        encoded = base64.b64encode(
            selected_file.read_bytes()
        ).decode("ascii")

    except Exception as error:
        print(
            f"\n{color('error:', RED)} "
            f"{t(language, 'copy_failed')} {error}"
        )
        return False

    message = f"Update {target_path}"

    # Use stdin for the API payload so the file content does not
    # become a huge shell argument.
    payload = json.dumps(
        {
            "message": message,
            "content": encoded,
            "sha": sha,
        },
        ensure_ascii=False,
    )

    print(
        f"\n{color(t(language, 'updating_file'), DIM)}"
    )

    result = subprocess.run(
        [
            "gh",
            "api",
            "-X",
            "PUT",
            f"repos/{repository}/contents/{target_path}",
            "--input",
            "-",
        ],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        return False

    return True


def update_test(language, platform):
    """
    Fast update:
    local file -> selected GitHub repository file,
    without cloning the repository.
    """
    selected_file = choose_file(
        language,
        platform
    )

    if selected_file is None:
        return

    repository = choose_github_repository(
        language
    )

    if repository is None:
        return

    target_path = choose_remote_file(
        language,
        repository
    )

    if target_path is None:
        return

    clear_screen()
    header(t(language, "update_test"))

    print(
        f"{color(t(language, 'file_selected'), DIM)} "
        f"{color(str(selected_file), CYAN)}"
    )

    print(
        f"{color(t(language, 'repository_selected'), DIM)} "
        f"{color(repository, CYAN)}"
    )

    print(
        f"{color(t(language, 'select_target_file'), DIM)} "
        f"{color(target_path, YELLOW)}"
    )

    success = update_file_via_github_api(
        selected_file,
        repository,
        target_path,
        language,
    )

    if success:
        save_history(
            "Update",
            target_path,
            "SUCCESS",
            repository
        )

        print(
            f"\n{color(t(language, 'update_success'), GREEN)}"
        )
    else:
        save_history(
            "Update",
            target_path,
            "FAILED",
            repository
        )

        print(
            f"\n{color(t(language, 'operation_failed'), RED)}"
        )

    pause(language)


# ═════════════════════════════════════
# DELETE
# ═════════════════════════════════════

def delete_test(language):
    repository = choose_github_repository(language)
    if repository is None:
        return

    clear_screen()
    header(t(language, "delete_test"))
    print(color(t(language, "cloning"), DIM))

    try:
        with tempfile.TemporaryDirectory(prefix="ghremote_") as temp:
            workspace = Path(temp) / "repo"

            if not clone_repository(repository, workspace, language):
                save_history("Delete", "-", "FAILED", repository)
                pause(language)
                return

            selected_file = choose_repo_file(language, workspace)
            if selected_file is None:
                return

            relative_name = str(selected_file.relative_to(workspace))
            print(
                f"\n{color(t(language, 'file_selected'), DIM)} "
                f"{color(relative_name, CYAN)}"
            )

            try:
                selected_file.unlink()
            except FileNotFoundError:
                print(f"\n{color(t(language, 'file_not_found'), RED)}")
                save_history("Delete", relative_name, "FAILED", repository)
                pause(language)
                return
            except Exception as error:
                print(f"\n{color(t(language, 'operation_failed'), RED)} {error}")
                save_history("Delete", relative_name, "FAILED", repository)
                pause(language)
                return

            print(f"\n{color(t(language, 'removing_file'), DIM)}")
            commit_and_push(
                workspace,
                relative_name,
                "Delete",
                language,
                repository,
            )

    except Exception as error:
        print(f"\n{color('error:', RED)} {error}")
        save_history("Delete", "-", "FAILED", repository)

    pause(language)


# ═════════════════════════════════════
# STATUS
# ═════════════════════════════════════

def repository_status(language):
    repository = choose_github_repository(language)
    if repository is None:
        return

    clear_screen()
    header(t(language, "repository_status"))
    print(color(t(language, "cloning"), DIM))

    try:
        with tempfile.TemporaryDirectory(prefix="ghremote_") as temp:
            workspace = Path(temp) / "repo"
            if not clone_repository(repository, workspace, language):
                pause(language)
                return

            result = run_git(workspace, "status", "--short")
            if result is None or result.returncode != 0:
                print(f"\n{color(t(language, 'repo_status_failed'), RED)}")
            elif result.stdout.strip():
                print(f"\n{color(t(language, 'repo_changes'), YELLOW)}")
            else:
                print(f"\n{color(t(language, 'repo_clean'), GREEN)}")
    except Exception as error:
        print(f"\n{color('error:', RED)} {error}")

    pause(language)


# ═════════════════════════════════════
# SETUP
# ═════════════════════════════════════

def choose_language():
    clear_screen()
    header("language / bahasa")
    print(f"{color('[1]', YELLOW)} {TEXT['id']['indonesia']}")
    print(f"{color('[2]', YELLOW)} {TEXT['en']['english']}")

    while True:
        choice = input(f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} ").strip()
        if choice == "1":
            return "id"
        if choice == "2":
            return "en"
        print(color("invalid choice.", RED))


def choose_platform(language):
    clear_screen()
    header(t(language, "select_device"))
    print(f"{color('[1]', YELLOW)} {t(language, 'android')}")
    print(f"{color('[2]', YELLOW)} {t(language, 'linux')}")

    while True:
        choice = input(f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} ").strip()
        if choice == "1":
            return "termux"
        if choice == "2":
            return "linux"
        print(color(t(language, "invalid_choice"), RED))


def command_available(command):
    return shutil.which(command) is not None


def check_dependencies(language):
    missing = [cmd for cmd in ("git", "gh") if not command_available(cmd)]
    if not missing:
        return True

    print(f"\n{color('error:', RED)}")
    for cmd in missing:
        print(f"- {cmd}")
    print()
    if "gh" in missing:
        print(color(t(language, "github_required"), RED))
    if "git" in missing:
        print(color("Git executable not found.", RED))
    pause(language)
    return False


# ═════════════════════════════════════
# MAIN MENU
# ═════════════════════════════════════

def main_menu(language, platform):
    while True:
        clear_screen()
        header(t(language, "menu"))

        print(
            f"{color(t(language, 'language'), DIM)}: "
            f"{color(TEXT[language]['indonesia'] if language == 'id' else TEXT[language]['english'], CYAN)}"
        )
        print(
            f"{color(t(language, 'device'), DIM)}: "
            f"{color(t(language, 'android') if platform == 'termux' else t(language, 'linux'), CYAN)}"
        )
        print()

        print(f"{color('[1]', YELLOW)} {t(language, 'upload_test')}")
        print(f"{color('[2]', YELLOW)} {t(language, 'update_test')}")
        print(f"{color('[3]', YELLOW)} {t(language, 'delete_test')}")
        print(f"{color('[4]', YELLOW)} {t(language, 'history')}")
        print(f"{color('[5]', YELLOW)} {t(language, 'status')}")
        print(f"{color('[6]', YELLOW)} {t(language, 'change_language')}")
        print(f"{color('[7]', YELLOW)} {t(language, 'change_device')}")
        print(f"{color('[0]', RED)} {t(language, 'exit')}")

        choice = input(f"\n{color(APP_NAME, CYAN)} {color('>', GREEN)} ").strip().lower()

        if choice == "1":
            upload_test(language, platform)
        elif choice == "2":
            update_test(language, platform)
        elif choice == "3":
            delete_test(language)
        elif choice == "4":
            show_history(language)
        elif choice == "5":
            repository_status(language)
        elif choice == "6":
            language = choose_language()
        elif choice == "7":
            platform = choose_platform(language)
        elif choice == "0" or choice == "x":
            clear_screen()
            print(color(t(language, "closed"), CYAN))
            break
        else:
            print(f"\n{color(t(language, 'invalid_choice'), RED)}")
            pause(language)


# ═════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════

def main():
    language = choose_language()
    platform = choose_platform(language)

    if not check_dependencies(language):
        return

    main_menu(language, platform)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print(color("GHremote interrupted.", YELLOW))
    except EOFError:
        print("\n")
        print(color("GHremote closed.", YELLOW))
