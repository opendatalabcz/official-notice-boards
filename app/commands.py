import click

from app.import_data import import_data


@click.command()
def import_all_data():
    import_data(force_import_all=True)


@click.command()
def import_new_data():
    import_data(force_import_all=False)


@click.command()  # TODO delete
def cli():
    import_data(force_import_all=True)
