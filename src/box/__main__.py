import click
from box.storage import commands as storage


@click.group()
def cli():
    pass


@cli.command()
def info():
    print("Info command")


cli.add_command(storage.storage)


def main():
    cli()


if __name__ == "__main__":
    main()
