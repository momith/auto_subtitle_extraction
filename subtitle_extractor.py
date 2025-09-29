import os
import json
import subprocess
from pathlib import Path
import time


WATCH_FOLDERS = os.getenv("WATCH_FOLDERS", "/path/to/directory/to/watch")
WATCH_FOLDERS = [d.strip() for d in WATCH_FOLDERS.split(",") if d.strip()]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))

SCRIPT_FILE = "./extract_subs.sh"
DB_FILE = "processed_mkv_files.json"


# --- Tracking ---
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        processed_files = json.load(f)  # Dictionary: {filepath: status}
else:
    processed_files = {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(processed_files, f, indent=2)

# --- Processing ---
def process_file(mkv_path):
    print(f"Processing {mkv_path}")
    status = "success"
    try:
        subprocess.run([SCRIPT_FILE, mkv_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error when processing {mkv_path}: {e}")
        status = "error"
    finally:
        processed_files[str(mkv_path)] = status
        save_db()

# --- Folder scanning ---
def scan_folders():
    for watch_dir in WATCH_FOLDERS:
        for root, dirs, files in os.walk(watch_dir):
            for file in files:
                if file.lower().endswith(".mkv"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    if full_path not in processed_files:
                        process_file(full_path)

# --- Main ---
if __name__ == "__main__":
    print(f"Watching folders: {WATCH_FOLDERS}")
    while True:
        scan_folders()
        time.sleep(CHECK_INTERVAL)
