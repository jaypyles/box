from box.utils import load_config, execute_command
from box.media.types import MediaConfig, MediaType
from rich.console import Console
from rich import print
import os
import shlex

console = Console()


def list_downloaded_files(config: MediaConfig):
    downloaded_files = os.listdir(config["download_path"])

    for idx, file in enumerate(downloaded_files):
        print(f"[cyan][file] {idx + 1} {file} [/cyan]")

    selected_file_idx = console.input("Select file to move: ")
    selected_file = downloaded_files[int(selected_file_idx) - 1]

    return selected_file


def list_media_folder(config: MediaConfig, media_type: MediaType):
    media_dirs = os.listdir(config[media_type + "_path"])

    for idx, dir in enumerate(media_dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    selected_dir_idx = console.input("[cyan]Select directory to move file to: [/cyan]")

    try:
        selected_dir = media_dirs[int(selected_dir_idx) - 1]
    except (IndexError, ValueError):
        creating_dir = console.input(
            "[cyan]Directory does not exist, create it? y/n (y): [/cyan]"
        )

        if creating_dir == "y":
            selected_dir = console.input("[cyan]Enter directory name: [/cyan]")
            os.makedirs(f"{config[media_type + '_path']}/{selected_dir}", exist_ok=True)

        else:
            return None

    return selected_dir


def place_into_media_folder(
    config: MediaConfig, media_type: MediaType, selected_dir: str, selected_file: str
):
    dirs = os.listdir(f"{config[media_type + '_path']}/{selected_dir}")

    for idx, dir in enumerate(dirs):
        print(f"[cyan][{idx + 1}] {dir}[/cyan]")

    inner_dir_idx = console.input("[cyan]Enter inner directory name: [/cyan]")
    inner_dir = None

    if not inner_dir_idx.isdigit():
        inner_dir = inner_dir_idx
        os.makedirs(
            f"{config[media_type + '_path']}/{selected_dir}/{inner_dir_idx}",
            exist_ok=True,
        )
    else:
        inner_dir = dirs[int(inner_dir_idx) - 1]

    print("Inner Dir: ", inner_dir)

    # Escape paths
    source_path = shlex.quote(os.path.join(config["download_path"], selected_file))
    destination_path = shlex.quote(
        os.path.join(config[media_type + "_path"], selected_dir, inner_dir)
    )

    # Execute command
    out, err = execute_command(f"sudo mv {source_path} {destination_path}")
    print(out)
    print(err)


def move_download_to_media(
    media_type: MediaType = "tv",
):
    config: MediaConfig = load_config("media/jellyfin")

    selected_file = list_downloaded_files(config)
    selected_dir = list_media_folder(config, media_type)

    if selected_dir is None:
        return

    place_into_media_folder(config, media_type, selected_dir, selected_file)
