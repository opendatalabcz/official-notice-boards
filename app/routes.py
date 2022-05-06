from typing import Any

from flask import render_template, request
from sqlalchemy import func, desc

from app import db
from app.language_translations import translate
from app.models import *
from app.utils.random_stuff import split_data_using_transpose
from app.utils.website import map_table_key_names

PAGE_SIZE = 100
SUB_PAGE_SIZE = 10
DEFAULT_LANGUAGE = 'cs'  # TODO move elsewhere


def view_index():
    return render_template('index.html')


def view_statistics():
    all_municipality_offices_with_extended_power_count = Municipality.query \
        .filter(Municipality.has_extended_competence == True).count()
    municipalities_with_extended_power_that_publish_boards = Municipality.query\
        .join(OfficialNoticeBoard, OfficialNoticeBoard.municipality_ruian == Municipality.ruian)\
        .filter(Municipality.has_extended_competence == True)\
        .group_by(Municipality.ruian)\
        .count()

    # extended_competence_publish_out_of_municipalities
    boards_by_municipalities_with_extended_power = OfficialNoticeBoard.query \
        .join(Municipality, OfficialNoticeBoard.municipality_ruian == Municipality.ruian) \
        .filter(Municipality.has_extended_competence == True) \
        .count()
    boards_by_municipalities = OfficialNoticeBoard.query \
        .join(Municipality, OfficialNoticeBoard.municipality_ruian == Municipality.ruian) \
        .count()

    documents_extensions_query = \
        db.session.query(func.count(NoticeDocument.file_extension).label('total_count'), NoticeDocument.file_extension)\
        .group_by(NoticeDocument.file_extension) \
        .order_by(desc('total_count')) \
        .limit(5).all()
    documents_extensions_data, documents_extensions_labels = map(list, zip(*documents_extensions_query))

    pdfs_w_text = \
        NoticeDocument.query.filter(NoticeDocument.attempted_extraction == True)\
        .filter(NoticeDocument.file_extension == 'pdf')\
        .filter(NoticeDocument.file_contains_no_text == False)\
        .count()
    pdfs_without_text = \
        NoticeDocument.query.filter(NoticeDocument.attempted_extraction == True) \
        .filter(NoticeDocument.file_extension == 'pdf') \
        .filter(NoticeDocument.file_contains_no_text == True) \
        .count()

    municipalities_with_most_unreachable_documents = \
        db.session.query(func.count(Municipality.name).label('total_count'), Municipality.name)\
        .join(OfficialNoticeBoard, Municipality.ruian == OfficialNoticeBoard.municipality_ruian)\
        .join(Notice, Notice.board_id == OfficialNoticeBoard.id)\
        .join(NoticeDocument, NoticeDocument.notice_id == Notice.id)\
        .filter(NoticeDocument.download_url_unreachable)\
        .group_by(Municipality.name)\
        .order_by(desc('total_count'))\
        .limit(10).all()
    municipalities_unreachable_documents_data, municipalities_unreachable_documents_labels = split_data_using_transpose(municipalities_with_most_unreachable_documents)

    municipalities_with_most_scanned_pdfs = \
        db.session.query(func.count(Municipality.name).label('total_count'), Municipality.name)\
        .join(OfficialNoticeBoard, Municipality.ruian == OfficialNoticeBoard.municipality_ruian)\
        .join(Notice, Notice.board_id == OfficialNoticeBoard.id)\
        .join(NoticeDocument, NoticeDocument.notice_id == Notice.id)\
        .filter(NoticeDocument.attempted_extraction == True) \
        .filter(NoticeDocument.file_extension == 'pdf') \
        .filter(NoticeDocument.file_contains_no_text == True) \
        .group_by(Municipality.name)\
        .order_by(desc('total_count'))\
        .limit(20).all()
    municipalities_scanned_pdfs_data, municipalities_scanned_pdfs_labels = split_data_using_transpose(municipalities_with_most_scanned_pdfs)

    # municipalities_with_most_missing_notices_iri = \
    #     db.session.query(func.count(Municipality.name).label('total_count'), Municipality.name) \
    #     .join(OfficialNoticeBoard, Municipality.ruian == OfficialNoticeBoard.municipality_ruian) \
    #     .join(Notice, Notice.board_id == OfficialNoticeBoard.id) \
    #     .filter(Notice.iri_missing == True) \
    #     .group_by(Municipality.name) \
    #     .order_by(desc('total_count')) \
    #     .limit(10).all()
    # municipalities_missing_notices_iri_data, municipalities_missing_notices_iri_labels = map(list, zip(*municipalities_with_most_missing_notices_iri))

    municipalities_no_comply_min_spec = \
        db.session.query(func.count(Municipality.name).label('total_count'), Municipality.name) \
        .join(OfficialNoticeBoard, Municipality.ruian == OfficialNoticeBoard.municipality_ruian) \
        .join(Notice, Notice.board_id == OfficialNoticeBoard.id) \
        .join(NoticeDocument, NoticeDocument.notice_id == Notice.id) \
        .filter((Notice.name_missing == True) | (Notice.iri_missing == True) | (Notice.url_missing == True) |
                (Notice.post_date_wrong_format == True) | (Notice.post_date_wrong_format == True) | \
                (OfficialNoticeBoard.office_name_missing == True) | \
                (OfficialNoticeBoard.download_url_missing == True) | \
                (OfficialNoticeBoard.download_url_unreachable == True)) \
        .group_by(Municipality.name) \
        .order_by(desc('total_count')) \
        .limit(20).all()
    municipalities_no_comply_min_spec_data, municipalities_no_comply_min_spec_labels = split_data_using_transpose(municipalities_no_comply_min_spec)
    # municipalities_no_comply_min_spec_data, municipalities_no_comply_min_spec_labels = map(list, zip(*municipalities_no_comply_min_spec))

    graph_data = {'extended_competence_publish_out_of_all': {'do_comply': municipalities_with_extended_power_that_publish_boards,
                                                             'dont_comply': all_municipality_offices_with_extended_power_count - municipalities_with_extended_power_that_publish_boards},
                  'extended_competence_publish_out_of_municipalities': {'extended': boards_by_municipalities_with_extended_power,
                                                                        'not_extended': boards_by_municipalities - boards_by_municipalities_with_extended_power},
                  'file_extensions_count': {'data': documents_extensions_data,
                                            'labels': documents_extensions_labels},
                  'PDFs_text': {'with': pdfs_w_text,
                                'without': pdfs_without_text},
                  'municipalities_unreachable_documents': {'data': municipalities_unreachable_documents_data,
                                                           'labels': municipalities_unreachable_documents_labels},
                  'municipalities_scanned_pdfs_documents': {'data': municipalities_scanned_pdfs_data,
                                                            'labels': municipalities_scanned_pdfs_labels},
                  # 'municipalities_missing_notices_iri': {'data': municipalities_missing_notices_iri_data,
                  #                                        'labels': municipalities_missing_notices_iri_labels},
                  'municipalities_no_comply_min_spec': {'data': municipalities_no_comply_min_spec_data,
                                                         'labels': municipalities_no_comply_min_spec_labels},
                  }

    return render_template('statistics.html', graph_data=graph_data)


def view_municipalities():
    page = request.args.get('page', 1, type=int)

    search = request.args.get('search', '')
    query = Municipality.query
    if len(search) > 0:
        query = query.filter(Municipality.name.ilike(f'%{search}%'))

    pagination = query.order_by(desc(Municipality.has_board)) \
        .order_by(desc(Municipality.has_extended_competence)) \
        .order_by(Municipality.name) \
        .paginate(page, per_page=PAGE_SIZE)

    records = pagination.items
    titles = map_table_key_names(Municipality)
    table_name = translate(DEFAULT_LANGUAGE, 'municipalities', capitalize_mode=2)
    return render_template('municipalities.html', pagination=pagination, records=records, titles=titles, table_name=table_name, Municipality=Municipality)


def view_municipality(municipality_ruian: int):
    municipality = Municipality.query.filter(Municipality.ruian == municipality_ruian).first()

    page = request.args.get('page', 1, type=int)
    pagination = OfficialNoticeBoard.query\
        .filter(OfficialNoticeBoard.municipality_ruian == municipality.ruian)\
        .paginate(page, per_page=1)
    boards = pagination.items

    graph_data = {}
    sorted_notices = []
    if len(boards) > 0:
        sorted_notices = Notice.query.filter(Notice.board_id == boards[0].id).order_by(desc(Notice.post_date)).all()
        graph_data = query_data_for_board_graphs(boards[0].id)


    return render_template('municipality.html', municipality=municipality, pagination=pagination, boards=boards, sorted_notices=sorted_notices, graph_data=graph_data)


# @cache.cached(timeout=50)
def view_boards():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = OfficialNoticeBoard.query
    if len(search) > 0:
        query = query.filter((OfficialNoticeBoard.name.ilike(f'%{search}%')) | \
                             (OfficialNoticeBoard.office_name.ilike(f'%{search}%')))

    pagination = query.order_by(OfficialNoticeBoard.name) \
        .paginate(page, per_page=PAGE_SIZE)

    records = pagination.items
    titles = map_table_key_names(OfficialNoticeBoard)
    table_name = translate(DEFAULT_LANGUAGE, 'official notice boards', capitalize_mode=1)
    return render_template('boards.html', pagination=pagination, records=records, titles=titles, table_name=table_name, OfficialNoticeBoard=OfficialNoticeBoard)


def query_data_for_board_graphs(board_id: int) -> dict[str, Any]:  # TODO move
    pdfs_w_text = NoticeDocument.query.join(Notice, Notice.id == NoticeDocument.notice_id)\
        .filter(Notice.board_id == board_id) \
        .filter(NoticeDocument.attempted_extraction == True) \
        .filter(NoticeDocument.file_extension == 'pdf') \
        .filter(NoticeDocument.file_contains_no_text == False) \
        .count()
    pdfs_without_text = NoticeDocument.query.join(Notice, Notice.id == NoticeDocument.notice_id)\
        .filter(Notice.board_id == board_id)\
        .filter(NoticeDocument.attempted_extraction == True)\
        .filter(NoticeDocument.file_extension == 'pdf')\
        .filter(NoticeDocument.file_contains_no_text == True)\
        .count()

    documents_extensions_query = db.session.query(func.count(NoticeDocument.file_extension).label('total_count'),
                                                  NoticeDocument.file_extension)\
        .join(Notice, Notice.id == NoticeDocument.notice_id)\
        .filter(Notice.board_id == board_id)\
        .group_by(NoticeDocument.file_extension) \
        .order_by(desc('total_count')) \
        .limit(5).all()
    # documents_extensions_data, documents_extensions_labels = map(list, zip(*documents_extensions_query))
    documents_extensions_data, documents_extensions_labels = split_data_using_transpose(documents_extensions_query)
    # documents_extensions_labels = list(filter(lambda x: x is not None, documents_extensions_labels))

    graph_data = {
        'file_extensions_count': {'data': documents_extensions_data,
                                  'labels': documents_extensions_labels},
        'PDFs_text': {'with': pdfs_w_text,
                      'without': pdfs_without_text}
        }
    return graph_data


def view_board(board_id: int):
    board = OfficialNoticeBoard.query.filter(OfficialNoticeBoard.id == board_id).first()
    sorted_notices = Notice.query.filter(Notice.board_id == board_id).order_by(desc(Notice.post_date)).all()

    graph_data = query_data_for_board_graphs(board_id)

    notice_table_name = translate(DEFAULT_LANGUAGE, 'notices', capitalize_mode=2)
    return render_template('board.html', board=board, notice_table_name=notice_table_name, sorted_notices=sorted_notices, graph_data=graph_data)


def view_documents():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    if search is None or len(search) == 0:
        pagination = NoticeDocument.query.paginate(page, per_page=PAGE_SIZE)
    else:
        pagination = NoticeDocument.query.filter(NoticeDocument.__ts_vector__.match(search)).paginate(page, per_page=PAGE_SIZE)

    records = pagination.items
    titles = map_table_key_names(NoticeDocument)

    table_name = translate(DEFAULT_LANGUAGE, 'documents', capitalize_mode=2)
    return render_template('documents.html', pagination=pagination, records=records, titles=titles, table_name=table_name)
