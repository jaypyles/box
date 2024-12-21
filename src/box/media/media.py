from box.utils import load_config, execute_command
from box.media.types import MediaConfig, MediaType
from rich.console import Console
from rich import print
import os
import shlex

from box.utils.command.utils import Shell

console = Console()


def move_to_path(
    config: MediaConfig, media_type: MediaType, selected_dir: str, selected_file: str
):
    source_path = os.path.join(config["download_path"], selected_file)
    destination_path = os.path.join(config[media_type + "_path"], selected_dir)

    quoted_source_path = shlex.quote(source_path)
    quoted_destination_path = shlex.quote(destination_path)

    print(f"Moving {quoted_source_path} to {quoted_destination_path}")

    return execute_command(
        f"sudo mv {quoted_source_path} {quoted_destination_path}", shell=Shell.BASH
    )


def list_downloaded_files(config: MediaConfig):
    downloaded_files = os.listdir(config["download_path"])

    for idx, file in enumerate(downloaded_files):
        print(f"[cyan][{idx + 1}] {file}[/cyan]")

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
            os.makedirs(
                shlex.quote(f"{config[media_type + '_path']}/{selected_dir}"),
                exist_ok=True,
            )

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
            shlex.quote(
                f"{config[media_type + '_path']}/{selected_dir}/{inner_dir_idx}"
            ),
            exist_ok=True,
        )
    else:
        inner_dir = dirs[int(inner_dir_idx) - 1]

    if inner_dir:
        selected_dir = f"{selected_dir}/{inner_dir}"

    out, err = move_to_path(config, media_type, selected_dir, selected_file)

    if err:
        print(f"[red]{err}[/red]")
    else:
        print(f"[green]{out}[/green]")


def move_download_to_media(
    media_type: MediaType = "tv",
):
    config: MediaConfig = load_config("media/jellyfin")

    selected_file = shlex.quote(list_downloaded_files(config))
    selected_dir = list_media_folder(config, media_type)

    if selected_dir is None:
        return

    selected_dir = shlex.quote(selected_dir)

    if media_type == "movie":
        out, err = move_to_path(config, media_type, selected_dir, selected_file)

        if err:
            print(f"[red]{err}[/red]")
        else:
            print(f"[green]{out}[/green]")

        return

    place_into_media_folder(config, media_type, selected_dir, selected_file)
