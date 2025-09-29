import os
import json
import subprocess
from pathlib import Path
import time


WATCH_FOLDER = os.getenv("WATCH_FOLDER", "/path/to/directory/to/watch")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))


SCRIPT_FILE = "./extract_subs.sh"
DB_FILE = "processed_mkv_files.json"


if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        processed_files = json.load(f)  # Dictionary: {filepath: status}
else:
    processed_files = {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(processed_files, f, indent=2)

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

def scan_folder():
    for root, dirs, files in os.walk(WATCH_FOLDER):
        for file in files:
            if file.lower().endswith(".mkv"):
                full_path = os.path.abspath(os.path.join(root, file))
                if full_path not in processed_files:
                    process_file(full_path)

if __name__ == "__main__":
    print(f"Watching folder: {WATCH_FOLDER}")
    while True:
        scan_folder()
        time.sleep(CHECK_INTERVAL)
