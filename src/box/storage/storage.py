import os
from rich import print


def determine_closest_size(size_in_bytes: float) -> str:
    """
    Convert a file size in bytes to a human-readable string.
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes:.2f} bytes"
    elif size_in_bytes < 1024**2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024**3:
        return f"{size_in_bytes / 1024**2:.2f} MB"
    elif size_in_bytes < 1024**4:
        return f"{size_in_bytes / 1024**3:.2f} GB"
    else:
        return f"{size_in_bytes / 1024**4:.2f} TB"


def calculate_size(path: str) -> int:
    """
    Get the size of a file or directory.
    If it's a file, return its size in bytes.
    If it's a directory, recursively calculate the total size of its contents.
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return sum(
            os.path.getsize(os.path.join(root, file))
            for root, _, files in os.walk(path)
            for file in files
        )
    else:
        return 0  # For invalid paths


def get_size(path: str):
    """
    Calculate and display the sizes of top-level files and directories.
    """
    total_size = 0
    size_map: dict[str, int] = {}

    try:
        top_level_entries = os.listdir(path)

    except (OSError, FileNotFoundError) as e:
        print(f"[bold red]Error accessing path: {path} ({e})[/bold red]")
        return

    for entry in top_level_entries:
        entry_path = os.path.join(path, entry)
        try:
            entry_size = calculate_size(entry_path)
            size_map[entry_path] = entry_size
            total_size += entry_size

        except (OSError, FileNotFoundError) as e:
            print(f"Error processing entry: {entry_path} ({e})")

    for path, size in size_map.items():
        print(f"[purple]{path}[/purple]: {determine_closest_size(size)}")

    print(f"\n[cyan]Total: {determine_closest_size(total_size)}[/cyan]")
