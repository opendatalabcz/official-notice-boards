import logging
import os.path
from signal import SIGINT
from time import sleep

from sqlalchemy import func

from app import db
from app.models import *
from app.sparql.mapper import fetch_mapper_data
from app.sparql.municipality import fetch_municipality_list
from app.sparql.official_notice_board import fetch_boards_data, fetch_board

# DOCUMENT_DIRECTORY = "../data/documents/"
DOCUMENT_DIRECTORY = "../../data/documents/"


def import_mapper():
    logging.info("Started mapper data import")
    for map_raw in fetch_mapper_data():
        db.session.add(Mapper.extract_from_dict(map_raw))
    logging.info("Finished mapper data import")


def import_municipalities():
    logging.info("Started municipality data import")
    for municipality_raw in fetch_municipality_list(is_part=False):
        municipality_record = Municipality.extract_from_dict(municipality_raw)
        db.session.add(municipality_record)
    logging.info("Finished municipality data import")

    logging.info("Started municipality part data import")
    for municipality_part_raw in fetch_municipality_list(is_part=True):
        municipality_part_record = Municipality.extract_from_dict(municipality_part_raw)
        db.session.add(municipality_part_record)
    logging.info("Finished municipality part data import")


def import_boards_list():
    logging.info("Started board list data import")
    for row in fetch_boards_data():
        db.session.add(OfficialNoticeBoard.extract_from_dict(row))
    logging.info("Finished board list data import")


def import_boards():
    logging.info("Started board data import")
    # download boards only for municipalities and municipality parts with their own ICO
    for board in OfficialNoticeBoard.query\
                    .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico)\
                    .join(Municipality, Mapper.ruian == Municipality.ruian)\
                    .all():
        # board.download(directory_path=DOCUMENT_DIRECTORY)  # probably generated, IDK
        board.download()
        for notice in board.notices:
            db.session.add(notice)  # TODO maybe swap order
            for document in notice.documents:
                db.session.add(document)  # TODO check if this is necessary

        # for notice_raw in fetch_board(board.download_url):
        #     notice_record = Notice.extract_from_dict(notice_raw)
        #     db.session.add(notice_record)
        #     for document in notice_record.documents:
        #         db.session.add(document)
        #     board.notices.append(notice_record)

        # break
    logging.info("Finished board data import")


def download_documents():
    logging.info("Started documents download")

    # random order, so that 1 server is not hit too often
    for document in NoticeDocument.query.order_by(func.random()).all():
        document.download(directory_path=DOCUMENT_DIRECTORY)
        # db.session.commit()

    logging.info("Finished documents download")


def extract_documents_text():
    logging.info("Started documents text extraction")
    for document in NoticeDocument.query.all():
        if document.extracted_text is None:
            print(f"\textracting {document}")
            document.extract_text()
            # db.session.commit()
        else:
            print(f"\tSKIPPING: {document}")
    logging.info("Finished documents text extraction")


def import_all():
    db.drop_all()
    db.create_all()
    import_mapper()
    import_municipalities()
    import_boards_list()
    import_boards()  # can be parallelized, but probably not worth it
    db.session.commit()

    download_documents()  # can be parallelized
    db.session.commit()

    extract_documents_text()  # can be parallelized
    db.session.commit()


if __name__ == '__main__':
    try:
        import_all()
    except KeyboardInterrupt:
        db.session.commit()
