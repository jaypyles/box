def fancy_list_files(files: list[str]):
    for idx, file in enumerate(files):
        print(f"[cyan][{idx + 1}] {file}[/cyan]")