import os
from box.utils import load_config
from box.media.types import MediaConfig

try:
    CONFIG: MediaConfig = load_config("media/jellyfin")
except Exception as e:
    print(f"[red]Error: {e}[/red]")
    exit(1)

DOWNLOAD_PATH = CONFIG["download_path"]
MOVIE_PATH = CONFIG["movie_path"]
TV_PATH = CONFIG["tv_path"]

download_files = []
movie_files = []
tv_files = []

try:
    download_files = os.listdir(DOWNLOAD_PATH)
    movie_files = os.listdir(MOVIE_PATH)
    tv_files = os.listdir(TV_PATH)
except Exception as e:
    print(f"[red]Error: {e}[/red]")
    exit(1)

DOWNLOAD_FILES: list[str] = download_files
MOVIE_FILES: list[str] = movie_files
TV_FILES: list[str] = tv_files
