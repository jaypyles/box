from box.utils import execute_command, fancy_list_files
from box.media.constants import DOWNLOAD_FILES, MOVIE_FILES, TV_FILES, CONFIG
from box.media.types import MediaConfig
from rich.console import Console
from rich import print
import os
import shlex

console = Console()

MEDIA_TYPES = {
    "1": "tv",
    "2": "movie",
}


def get_files(media_type: str):
    if media_type == "tv":
        fancy_list_files(TV_FILES)
    elif media_type == "movie":
        fancy_list_files(MOVIE_FILES)
    elif media_type == "download":
        fancy_list_files(DOWNLOAD_FILES)


def list_downloaded_files():
    fancy_list_files(DOWNLOAD_FILES)

    selected_file_idx = console.input("Select file to move: ")
    selected_file = DOWNLOAD_FILES[int(selected_file_idx) - 1]

    return selected_file


def determine_type_of_file():
    type_of_file = console.input(
        """Is this a:\n[cyan][1] Episode/Season[/cyan]\n[cyan][2] Movie[/cyan]\n[cyan]Enter the number of the type of file: [/cyan]"""
    )

    return type_of_file


def list_season_folder(media_path: str):
    media_dirs = os.listdir(media_path)
    fancy_list_files(media_dirs)

    season_idx = console.input("Enter the number of the season: ")

    if not season_idx:
        return None

    try:
        season_dir = media_dirs[int(season_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{season_idx}")
        season_dir = season_idx

    return season_dir


def list_show_folder(media_type: str):
    media_path = CONFIG.get(media_type + "_path", "")

    if not media_path or not os.path.isdir(media_path):
        print(f"[red]Error: Invalid path for media type '{media_type}'.[/red]")
        return

    media_dirs = os.listdir(media_path)
    fancy_list_files(media_dirs)

    show_idx = console.input("Select a show to move the episode to: ")

    try:
        show_dir = media_dirs[int(show_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{show_idx}")
        show_dir = show_idx

    season_dir = list_season_folder(f"{media_path}/{show_dir}")
    path = f"{media_path}/{show_dir}"

    if season_dir:
        path = f"{path}/{season_dir}"

    return path


def list_movie_folder(config: MediaConfig, media_type: str):
    media_path = config.get(media_type + "_path", "")

    if not media_path or not os.path.isdir(media_path):
        print(f"[red]Error: Invalid path for media type '{media_type}'.[/red]")
        return

    movie_dirs = os.listdir(media_path)
    fancy_list_files(movie_dirs)

    selected_movie_idx = console.input("Select a movie folder to move to: ")

    try:
        selected_movie = movie_dirs[int(selected_movie_idx) - 1]
    except (IndexError, ValueError):
        _ = execute_command(f"mkdir {media_path}/{selected_movie_idx}")
        selected_movie = selected_movie_idx

    return f"{media_path}/{selected_movie}"


def move_episode():
    return list_show_folder("tv")


def move_movie(config: MediaConfig):
    return list_movie_folder(config, "movie")


def move_download_to_media():
    selected_file = list_downloaded_files()
    full_selected_file = f"{CONFIG['download_path']}/{selected_file}"

    type_of_file = determine_type_of_file()
    media_type = MEDIA_TYPES[type_of_file]

    destination_dir = None

    if media_type == "tv":
        destination_dir = move_episode()
        if destination_dir:
            print(f"Moving {full_selected_file} to {destination_dir}")
            out, err = execute_command(
                f"sudo mv {shlex.quote(full_selected_file)} {shlex.quote(destination_dir)}"
            )

            print(out)
            print(err)

    elif media_type == "movie":
        destination_dir = move_movie(CONFIG)
        if destination_dir:
            for file in os.listdir(full_selected_file):
                file_path = f"{full_selected_file}/{file}"
                print(f"Moving {file_path} to {destination_dir}")
                out, err = execute_command(
                    f"sudo mv {shlex.quote(file_path)} {shlex.quote(destination_dir)}"
                )

                print(out)
                print(err)

            _ = execute_command(f"sudo rm -rf {shlex.quote(full_selected_file)}")
