import click
from box.media.media import move_download_to_media


@click.group()
def media():
    pass


@media.command()
def move():
    move_download_to_media()
