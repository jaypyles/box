import click

from box.actual.actual import actual as actual_command


@click.group()
def actual():
    pass


@actual.command()
def email():
    actual_command()
