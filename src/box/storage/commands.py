import click

from box.storage.storage import get_size


@click.group()
def storage():
    pass


@storage.command()
@click.argument("path", required=False, default=".")
def size(path: str):
    get_size(path)
