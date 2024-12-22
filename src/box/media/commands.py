import click
from box.media.media import move_download_to_media, get_files


@click.group()
def media():
    pass


@media.command()
def move():
    move_download_to_media()


@media.command()
@click.argument("media_type", choices=["tv", "movie", "download"])
def list(media_type: str):
    get_files(media_type)
