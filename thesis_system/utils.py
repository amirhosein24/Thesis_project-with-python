import os, shutil, datetime
from pathlib import Path

BASE_FILES = os.path.join(os.path.dirname(__file__), "..", "files")

def copy_file_to_storage(src_path, subfolder):
    if not os.path.exists(src_path):
        raise FileNotFoundError("source file not found: " + src_path)
    dest_dir = os.path.join(BASE_FILES, subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, f"{int(datetime.datetime.now().timestamp())}_{filename}")
    shutil.copy(src_path, dest_path)
    return dest_path

def days_since(date_str):
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return (datetime.datetime.now() - dt).days