import click

from box.media import commands as media
from box.storage import commands as storage
from box.actual import commands as actual


@click.group()
def cli():
    pass


@cli.command()
def info():
    print("Info command")


cli.add_command(storage.storage)
cli.add_command(media.media)
cli.add_command(actual.actual)


def main():
    cli()


if __name__ == "__main__":
    main()
