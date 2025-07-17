import os

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def is_valid_youtube_url(url):
    return url.startswith("http://") or url.startswith("https://")
