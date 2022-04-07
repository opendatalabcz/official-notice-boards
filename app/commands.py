import click

from app.import_data import import_all


@click.command()
def import_data():
    import_all()
    # import_all(download_documents=True, extract_documents_text=True)
