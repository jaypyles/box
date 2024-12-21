import click
from box.media.types import MediaType
from box.media.media import move_download_to_media


@click.group()
def media():
    pass


@media.command()
@click.argument("path")
@click.option(
    "--type", type=click.Choice(["movie", "tv"]), default="tv", required=False
)
def move(path: str, media_type: MediaType):
    move_download_to_media(path, media_type)
