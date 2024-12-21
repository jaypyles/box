import click
from box.media.types import MediaType
from box.media.media import move_download_to_media


@click.group()
def media():
    pass


@media.command()
@click.option(
    "--media_type", type=click.Choice(["movie", "tv"]), default="tv", required=False
)
def move(media_type: MediaType):
    move_download_to_media(media_type)
