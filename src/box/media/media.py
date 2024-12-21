from box.utils import load_config, execute_command
from box.media.types import MediaConfig, MediaType
from rich.console import Console
from rich import print
import os

console = Console()


def move_download_to_media(
    path: str,
    media_type: MediaType = "tv",
):
    config: MediaConfig = load_config("media/jellyfin")

    downloaded_files = os.listdir(path)

    for idx, file in enumerate(downloaded_files):
        print(f"[cyan][file] {idx + 1} {file} [/cyan]")

    selected_file = console.input("Select file to move: ")

    media_dirs = os.listdir(config[media_type + "_path"])

    for dir in media_dirs:
        print(f"[cyan][dir] {dir} [/cyan]")

    selected_dir = console.input("[cyan]Select directory to move file to: [/cyan]")
    create_inner_dir = console.input("[cyan]Create inner directory? y/n (y): [/cyan]")

    if not create_inner_dir:
        create_inner_dir = "y"

    if create_inner_dir == "y":
        inner_dir = console.input("[cyan]Enter inner directory name: [/cyan]")
        os.makedirs(
            f"{config[media_type + '_path']}/{selected_dir}/{inner_dir}",
            exist_ok=True,
        )

        _ = execute_command(
            f"mv {path}/{selected_file} {config[media_type + '_path']}/{selected_dir}/{inner_dir}"
        )
    else:
        _ = execute_command(
            f"mv {path}/{selected_file} {config[media_type + '_path']}/{selected_dir}"
        )
