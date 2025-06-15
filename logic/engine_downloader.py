import os
import platform
import stat
import requests
import zipfile
import tarfile
import shutil

ASSETS_DIR = "assets/engine"
STOCKFISH_DIR = "engines"

STOCKFISH_URLS = {
    "Windows": "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-avx2.zip",
    "Linux": "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar",
}

STOCKFISH_EXE_NAME = {
    "Windows": "stockfish-windows-x86-64-avx2.exe",
    "Linux": "stockfish-linux-x86-64-avx2",
}


def is_nixos():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.strip() == "ID=nixos":
                    return True
    except FileNotFoundError:
        pass
    return False


def find_stockfish_in_assets(system):
    exe_name = STOCKFISH_EXE_NAME.get(system)
    if not exe_name:
        return None

    path = os.path.join(ASSETS_DIR, exe_name)
    if os.path.isfile(path):
        return os.path.abspath(path)
    return None


def get_stockfish_path():
    system = platform.system()

    # Handle NixOS separately
    if system == "Linux" and is_nixos():
        path = shutil.which("stockfish")
        if path and os.path.isfile(path):
            return os.path.abspath(path)
        else:
            raise RuntimeError(
                "Stockfish executable not found in PATH on NixOS.\n"
                "Please install it via `nix-shell -p stockfish` or through your system configuration."
            )

    # Check local assets
    asset_path = find_stockfish_in_assets(system)
    if asset_path:
        return asset_path

    # Fall back to download
    url = STOCKFISH_URLS.get(system)
    exe_name = STOCKFISH_EXE_NAME.get(system)

    if not url or not exe_name:
        raise RuntimeError(f"Unsupported OS: {system}")

    os.makedirs(STOCKFISH_DIR, exist_ok=True)
    archive_path = os.path.join(STOCKFISH_DIR, os.path.basename(url))
    exe_path = os.path.join(STOCKFISH_DIR, exe_name)

    if not os.path.exists(exe_path):
        print(f"Downloading {url} ...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(archive_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print("Extracting archive...")

        if archive_path.endswith(".zip"):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(STOCKFISH_DIR)

                extracted_path = None
                for name in zip_ref.namelist():
                    if name.endswith(".exe") and "stockfish" in name.lower():
                        extracted_path = os.path.join(STOCKFISH_DIR, name)
                        break

                if not extracted_path or not os.path.exists(extracted_path):
                    raise RuntimeError(f"Expected extracted binary not found: {extracted_path}")

                if os.path.exists(exe_path):
                    os.remove(exe_path)
                os.rename(extracted_path, exe_path)

        elif archive_path.endswith(".tar"):
            with tarfile.open(archive_path, 'r') as tar_ref:
                tar_ref.extractall(STOCKFISH_DIR)

            extracted_path = None
            for root, _, files in os.walk(STOCKFISH_DIR):
                for file in files:
                    if file == exe_name:
                        extracted_path = os.path.join(root, file)
                        break

            if not extracted_path or not os.path.exists(extracted_path):
                raise RuntimeError(f"Expected extracted binary not found: {extracted_path}")

            if os.path.exists(exe_path):
                os.remove(exe_path)
            os.rename(extracted_path, exe_path)

        else:
            raise RuntimeError("Unknown archive format")

        os.remove(archive_path)

        if system != "Windows":
            st = os.stat(exe_path)
            os.chmod(exe_path, st.st_mode | stat.S_IEXEC)

    return os.path.abspath(exe_path)


if __name__ == "__main__":
    try:
        path = get_stockfish_path()
        print("Stockfish engine ready at:", path)
    except Exception as e:
        print("Failed to prepare Stockfish engine:")
        print(str(e))
