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
        """Is this a:\n[cyan][1] Episode File[/cyan]\n[cyan][2] Movie File[/cyan]\n[cyan][3] Movie Folder[/cyan]\n[cyan][4] Season Folder[/cyan]\n[cyan]Enter the number of the type of file: [/cyan]"""
    )

    return type_of_file


def list_season_folder(media_path: str):
    media_dirs = os.listdir(media_path)

    for idx, dir in enumerate(media_dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    print(f"Select a season to move the episode to: ")

    season_idx = console.input("Enter the number of the season: ")

    if not season_idx:
        return media_path

    try:
        season_dir = media_dirs[int(season_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{season_idx}")
        season_dir = season_idx

    return season_dir


def list_show_folder(config: MediaConfig, media_type: str):
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

    season_dir = list_season_folder(f"{media_path}/{show_dir}")

    return season_dir


def list_movie_folder(config: MediaConfig, media_type: str):
    media_path = config.get(media_type + "_path", "")

    if not media_path or not os.path.isdir(media_path):
        print(f"[red]Error: Invalid path for media type '{media_type}'.[/red]")
        return

    movie_dirs = os.listdir(media_path)

    for idx, dir in enumerate(movie_dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    selected_movie_idx = console.input("Select a movie folder to move to: ")
    try:
        selected_movie = movie_dirs[int(selected_movie_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{selected_movie_idx}")
        selected_movie = selected_movie_idx

    return selected_movie


def move_episode(config: MediaConfig):
    return list_show_folder(config, "tv")


def move_movie(config: MediaConfig):
    return list_movie_folder(config, "movie")


def move_season(config: MediaConfig):
    return list_show_folder(config, "tv")


def move_download_to_media():
    config: MediaConfig = load_config("media/jellyfin")
    type_of_file = determine_type_of_file()
    media_type = MEDIA_TYPES[type_of_file]

    selected_file = list_downloaded_files(config)

    destination_dir = None

    if media_type == "tv":
        destination_dir = move_episode(config)

    elif media_type == "movie":
        destination_dir = move_movie(config)
        if destination_dir:
            for file in os.listdir(selected_file):
                file_path = f"{selected_file}/{file}"
                _ = execute_command(
                    f"sudo mv {shlex.quote(file_path)} {shlex.quote(destination_dir)}"
                )

    elif media_type == "season":
        destination_dir = move_season(config)

    # execute_command(f"mv {selected_file} {destination_dir}")
