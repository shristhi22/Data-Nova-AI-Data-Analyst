import os
import json
import shutil

UPLOAD_FOLDER = "uploads"
HISTORY_FILE = "uploads/history.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(uploaded_file):
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    history = load_history()

    if uploaded_file.name in history:
        history.remove(uploaded_file.name)

    history.insert(0, uploaded_file.name)

    history = history[:10]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

    return filepath


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def get_file_path(filename):
    return os.path.join(UPLOAD_FOLDER, filename)