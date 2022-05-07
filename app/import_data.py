from flask import current_app
from sqlalchemy import func, inspect

from app import db, create_app
from app.models import *
from app.sparql.mapper import fetch_ruian_2_ico_mapper, fetch_extended_power_municipalities_list
from app.sparql.municipality import fetch_municipality_list
from app.sparql.official_notice_board import fetch_boards_data, fetch_board

# DOCUMENT_DIRECTORY = "../data/documents/"
DOCUMENT_DIRECTORY = "../../data/documents/"


def first_import() -> bool:
    inspector = inspect(db.engine)
    if not inspector.has_table("municipality"):
        return True

    # municipalities_imported = bool(Municipality.query.count() > 6000)  # not necessary, because of the next one
    ruian_2_ico_mapped = bool(Municipality.query.filter(Municipality.ico != None).count() > 6000)
    extended_power_mapped = bool(Municipality.query.filter(Municipality.has_extended_competence == True).count() > 200)
    return not (ruian_2_ico_mapped and extended_power_mapped)


def import_municipalities():
    current_app.logger.info("Started municipality data import")
    for municipality_raw in fetch_municipality_list(is_part=False):
        municipality_record = Municipality.extract_from_dict(municipality_raw)
        db.session.add(municipality_record)
    current_app.logger.info("Finished municipality data import")

    current_app.logger.info("Started municipality part data import")
    for municipality_part_raw in fetch_municipality_list(is_part=True):
        municipality_part_record = Municipality.extract_from_dict(municipality_part_raw)
        db.session.add(municipality_part_record)
    current_app.logger.info("Finished municipality part data import")


def map_municipalities_ruian_2_ico():
    current_app.logger.info("Started mapper data import")
    for ruian, ico in fetch_ruian_2_ico_mapper():
        municipality_record = Municipality.query.filter(Municipality.ruian == ruian).first()
        if municipality_record is None:
            current_app.logger.warning("Cannot ")
        municipality_record.ico = ico
    current_app.logger.info("Finished mapper data import")


def mark_municipalities_with_extended_power():
    current_app.logger.info("Started mapper data import")
    for ruian in fetch_extended_power_municipalities_list():
        municipality_record = Municipality.query.filter(Municipality.ruian == ruian).first()
        if municipality_record is not None:
            municipality_record.has_extended_competence = True
    current_app.logger.info("Finished mapper data import")


def import_boards_list():
    current_app.logger.info("Started board list data import")

    for row in fetch_boards_data():
        new_board = OfficialNoticeBoard.extract_from_dict(row)
        # new_boards.append(new_board)
        existing_boards = OfficialNoticeBoard.query\
            .filter(OfficialNoticeBoard.download_url == new_board.download_url and
                    OfficialNoticeBoard.office_name == new_board.office_name) \
            .order_by(OfficialNoticeBoard.id)\
            .all()
        if len(existing_boards) > 0:
            current_app.logger.info("Found existing identical board, office_name='%s', download_url=%s", new_board.office_name, new_board.download_url)
            if len(existing_boards) > 1:
                current_app.logger.error("Multiple existing identical boards found, office_name='%s', download_url=%s", new_board.office_name, new_board.download_url)

        # brand new board
        elif len(existing_boards) == 0:
            current_app.logger.info("Found new board")
            db.session.add(new_board)
            related_municipalities = Municipality.query.filter(Municipality.ico == new_board.ico).all()
            for m in related_municipalities:
                m.boards.append(new_board)
                m.has_board = True

    current_app.logger.info("Finished board list data import")


def import_boards(only_municipality_boards: bool):
    current_app.logger.info("Started board data import")

    query = OfficialNoticeBoard.query
    if only_municipality_boards:
        current_app.logger.info("Importing only municipality boards")
        query = query.join(Municipality, OfficialNoticeBoard.municipality_ruian == Municipality.ruian)

    for board in query.all():
        board.download()
        for notice_record in board.notices:
            db.session.add(notice_record)
            for document in notice_record.documents:
                db.session.add(document)
        # break
    current_app.logger.info("Finished board data import")


def download_extract_documents(directory_path: str, delete_files: bool):
    current_app.logger.info("Started documents download and text extraction")

    # random order, so that 1 server is not hit too often
    for document in NoticeDocument.query\
            .filter(NoticeDocument.attempted_download == False)\
            .order_by(func.random())\
            .all():

        document.download(directory_path=directory_path)
        # if document.download(directory_path=directory_path):  # TODO maybe switch to this
        document.extract_text()
        if delete_files:
            document.delete_file()
        db.session.commit()  # TODO might delete this

    current_app.logger.info("Finished documents download and text extraction")


def import_data(force_import_all: bool):

    app = create_app()
    app.app_context().push()
    current_app.logger.info("After pushing APP context")

    if first_import() or force_import_all:
        current_app.logger.info("Importing all data")
        db.drop_all()
        db.create_all()
        current_app.logger.info("Dropped and created database")

        import_municipalities()
        map_municipalities_ruian_2_ico()
        mark_municipalities_with_extended_power()

    import_boards_list()
    import_boards(only_municipality_boards=current_app.config["IMPORT_ONLY_MUNICIPALITY_BOARDS"])

    db.session.commit()

    download_extract_documents(directory_path=current_app.config["DOWNLOADED_DOCUMENT_DIRECTORY"],
                               delete_files=current_app.config["DELETE_DOCUMENTS_AFTER_EXTRACTION"])
    db.session.commit()


if __name__ == '__main__':
    import_data(force_import_all=False)
