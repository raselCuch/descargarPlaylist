import yt_dlp
from constants import YDL_OPTS_TEMPLATE, DOWNLOAD_FOLDER
from utils import ensure_folder_exists

def download_audio_from_url(url):
    ensure_folder_exists(DOWNLOAD_FOLDER)
    with yt_dlp.YoutubeDL(YDL_OPTS_TEMPLATE) as ydl:
        ydl.download([url])
