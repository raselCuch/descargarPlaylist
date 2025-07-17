APP_NAME = "Soft Download Music"
VERSION = "1.0"
AUTHOR = "Rasel"

DOWNLOAD_FOLDER = "downloads"
DEFAULT_AUDIO_FORMAT = "mp3"
YDL_OPTS_TEMPLATE = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': DEFAULT_AUDIO_FORMAT,
        'preferredquality': '192',
    }],
    'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    'quiet': True
}
