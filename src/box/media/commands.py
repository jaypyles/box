import click
from box.media.media import move_download_to_media, get_files


@click.group()
def media():
    pass


@media.command()
def move():
    move_download_to_media()


@media.command()
@click.option(
    "--media-type",
    type=click.Choice(["tv", "movie", "download"]),
    required=True,
    help="Type of media to list.",
)
def list(media_type: str):
    get_files(media_type)
