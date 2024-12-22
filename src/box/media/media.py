from box.utils import load_config, execute_command
from box.media.types import MediaConfig, MediaType
from rich.console import Console
from rich import print
import os
import shlex

console = Console()

MEDIA_TYPES = {
    "1": "tv",
    "2": "movie",
    "3": "tv",
}


def list_downloaded_files(config: MediaConfig):
    downloaded_files = os.listdir(config["download_path"])

    for idx, file in enumerate(downloaded_files):
        print(f"[cyan][{idx + 1}] {file}[/cyan]")

    selected_file_idx = console.input("Select file to move: ")
    selected_file = downloaded_files[int(selected_file_idx) - 1]

    return selected_file


def determine_type_of_file():
    type_of_file = console.input(
        """Is this a:
        [cyan][1] Episode File[/cyan]
        [cyan][2] Movie File[/cyan]
        [cyan][3] Movie Folder[/cyan]
        [cyan][4] Season Folder[/cyan]
        [cyan]Enter the number of the type of file: [/cyan]"""
    )

    return type_of_file


def list_inner_media_folder(media_path: str):
    media_dirs = os.listdir(media_path)

    for idx, dir in enumerate(media_dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    print(f"Select a season to move the episode to: ")

    season_idx = console.input("Enter the number of the season: ")
    season_dir = media_dirs[int(season_idx) - 1]

    return season_dir


def list_media_folder(config: MediaConfig, media_type: str):
    media_path = config.get(media_type + "_path", "")
    if not media_path or not os.path.isdir(media_path):
        print(f"[red]Error: Invalid path for media type '{media_type}'.[/red]")
        return

    media_dirs = os.listdir(media_path)

    for idx, dir in enumerate(media_dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    show_idx = console.input("Select a show to move the episode to: ")
    try:
        show_dir = media_dirs[int(show_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{show_idx}")
        show_dir = show_idx

    season_dir = list_inner_media_folder(f"{media_path}/{show_dir}")

    return season_dir


def move_episode(config: MediaConfig, selected_file: str):
    list_media_folder(config, "tv")


def move_movie(config: MediaConfig, selected_file: str):
    list_media_folder(config, "movie")


def move_season(config: MediaConfig, selected_file: str):
    list_media_folder(config, "tv")


def move_download_to_media():
    config: MediaConfig = load_config("media/jellyfin")
    type_of_file = determine_type_of_file()
    media_type = MEDIA_TYPES[type_of_file]

    selected_file = list_downloaded_files(config)

    if media_type == "tv":
        move_episode(config, selected_file)
    elif media_type == "movie":
        move_movie(config, selected_file)
    elif media_type == "season":
        move_season(config, selected_file)
