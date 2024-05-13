import logging
import os.path
import random

import pytest
from sqlalchemy import func

from app import db
from app.models import *
from app.sparql.mapper import fetch_mapper_data
from app.sparql.municipality import fetch_municipality_list
from app.sparql.official_notice_board import fetch_boards_data

# DOCUMENT_DIRECTORY = "./integration/tmp_documents"
DOCUMENT_DIRECTORY = "tests/integration/tmp_documents/"

FETCH_BOARDS_COUNT = 10
FETCH_DOCUMENTS_COUNT = 20

  # TODO check out https://pypi.org/project/vcrpy/

# TODO set separate database for testing


@pytest.fixture(scope="module")
def tmp_directory_cleaner():
    if not os.path.isdir(DOCUMENT_DIRECTORY):
        os.mkdir(DOCUMENT_DIRECTORY)
    for file in os.listdir(DOCUMENT_DIRECTORY):
        os.remove(os.path.join(DOCUMENT_DIRECTORY, file))


def _import_mapper():
    logging.info("Started mapper data import")
    for map_raw in fetch_mapper_data():
        db.session.add(Mapper.extract_from_dict(map_raw))
    logging.info("Finished mapper data import")


def _import_municipalities():
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


def _import_boards_list():
    logging.info("Started board list data import")
    for row in random.sample(fetch_boards_data(), FETCH_BOARDS_COUNT):
        db.session.add(OfficialNoticeBoard.extract_from_dict(row))
    logging.info("Finished board list data import")


def _import_boards():
    logging.info("Started board data import")
    # download boards only for municipalities and municipality parts with their own ICO
    for board in OfficialNoticeBoard.query\
                    .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico)\
                    .join(Municipality, Mapper.ruian == Municipality.ruian)\
                    .all():
        # board.download(directory_path=DOCUMENT_DIRECTORY)  # probably generated, IDK
        board.download()
        for notice in board.notices:
            db.session.add(notice)
            for document in notice.documents:
                db.session.add(document)
        # break
    logging.info("Finished board data import")


def _download_documents():  # TODO check why for all had url
    logging.info("Started documents download")

    # random order, so that 1 server is not hit too often
    for document in NoticeDocument.query.order_by(func.random()).limit(FETCH_DOCUMENTS_COUNT).all():
        document.download(directory_path=DOCUMENT_DIRECTORY)

    logging.info("Finished documents download")


def _extract_documents_text():
    logging.info("Started documents text extraction")
    for document in NoticeDocument.query.filter(NoticeDocument.attempted_download == True).all():
        document.extract_text()
    logging.info("Finished documents text extraction")


@pytest.fixture(scope="module")
# @pytest.mark.vcr()
def test_import_all(tmp_directory_cleaner):
    db.drop_all()
    db.create_all()
    _import_mapper()
    _import_municipalities()
    _import_boards_list()
    _import_boards()  # can be parallelized, but probably not worth it
    _download_documents()  # can be parallelized
    _extract_documents_text()  # can be parallelized
    db.session.commit()


@pytest.fixture(scope="function")
def new_transaction():
    db.session.close()


def test_import_mapper(test_import_all, new_transaction):
    assert 6300 < Mapper.query.count()
    assert 6000 < Mapper.query.filter(Mapper.ico != None).filter(Mapper.ruian != None).count() < 6350
    assert 50 < Mapper.query.filter(Mapper.ico == None).filter(Mapper.ruian != None).count() < 200


def test_import_municipality(test_import_all, new_transaction):
    assert Municipality.query.count() > 6300


def test_import_boards_list(test_import_all, new_transaction):
    assert OfficialNoticeBoard.query.count() == FETCH_BOARDS_COUNT


def test_import_boards(test_import_all, new_transaction):
    # query based on https://stackoverflow.com/questions/69116955/flask-sqlalchemy-filter-by-count-of-relationship-objects
    boards_with_some_notices = db.session.query(OfficialNoticeBoard,).\
        outerjoin(OfficialNoticeBoard.notices).\
        group_by(OfficialNoticeBoard.id).\
        having(func.count(Notice.id) > 0).\
        count()
    assert 0 < boards_with_some_notices <= FETCH_BOARDS_COUNT
    assert Notice.query.count() > FETCH_BOARDS_COUNT
    assert NoticeDocument.query.count() > FETCH_BOARDS_COUNT


def test_download_documents(test_import_all, new_transaction):
    assert 0 < NoticeDocument.query.filter(NoticeDocument.attempted_download == True).count() <= FETCH_DOCUMENTS_COUNT
    assert 0 <= NoticeDocument.query.filter(NoticeDocument.download_url_missing == True).count() <= FETCH_DOCUMENTS_COUNT


def test_extract_documents_text(test_import_all, new_transaction):
    assert 0 < NoticeDocument.query.filter(func.length(NoticeDocument.extracted_text) > FETCH_DOCUMENTS_COUNT/4).count() <= FETCH_DOCUMENTS_COUNT
