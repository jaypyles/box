from rich import print


def fancy_list_files(files: list[str]):
    for idx, file in enumerate(files):
        print(f"[bold cyan][{idx + 1}] {file}[/bold cyan]")
