from flask import render_template, request
from sqlalchemy import func, desc

from app import db
from app.language_translations import translate
from app.models import *
from app.utils.website import filter_model_to_table, map_table_key_names

PAGE_SIZE = 100
SUB_PAGE_SIZE = 10
DEFAULT_LANGUAGE = 'cs'  # TODO move elsewhere


def view_index():

    # # get counts of notices per municipality
    # db.session.query(func.count(Notice.id)) \
    #     .select_from(OfficialNoticeBoard)\
    #     .outerjoin(Notice) \
    #     .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
    #     .join(Municipality, Mapper.ruian == Municipality.ruian) \
    #     .group_by(OfficialNoticeBoard.id).all()

    all_boards_count = OfficialNoticeBoard.query.count()
    boards_by_municipalities = OfficialNoticeBoard.query \
        .join(Municipality, OfficialNoticeBoard.municipality_ruian == Municipality.ruian) \
        .count()
    boards_rest_count = all_boards_count - boards_by_municipalities

    all_municipality_offices_count = Municipality.query.count()
    municipalities_rest_count = all_municipality_offices_count - boards_by_municipalities

    documents_extensions_query = db.session.query(func.count(NoticeDocument.file_extension).
                           label('total_count'),
                           NoticeDocument.file_extension)\
        .group_by(NoticeDocument.file_extension)\
        .limit(10).all()
    documents_extensions_query.sort(reverse=True)
    documents_extensions_data, documents_extensions_labels = map(list, zip(*documents_extensions_query))
    documents_extensions_labels = ['None' if x is None else x for x in documents_extensions_labels]

    # page_name = translate(DEFAULT_LANGUAGE, 'graphs', capitalize_mode=2)
    page_name = 'About'
    return render_template('index.html',
                           page_name=page_name,
                           boards_by_municipalities=boards_by_municipalities,
                           boards_rest_count=boards_rest_count,
                           municipalities_rest_count=municipalities_rest_count,
                           documents_extensions_data=documents_extensions_data,
                           documents_extensions_labels=documents_extensions_labels)


def view_municipalities():
    page = request.args.get('page', 1, type=int)
    # Municipality.query.filter(Municipality.name.like("%Peruc%")).all()

    search = request.args.get('search')
    if search is None or len(search) == 0:
        pagination = Municipality.query \
            .order_by(desc(Municipality.has_board)) \
            .order_by(Municipality.name) \
            .paginate(page, per_page=PAGE_SIZE)
    else:
        pagination = Municipality.query\
            .filter(Municipality.name.ilike(f'%{search}%'))\
            .order_by(desc(Municipality.has_board)) \
            .order_by(Municipality.name) \
            .paginate(page, per_page=PAGE_SIZE)
    # pagination = Municipality.query.paginate(page, per_page=PAGE_SIZE)
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

    boards_table_name = translate(DEFAULT_LANGUAGE, 'official notice boards', capitalize_mode=2)
    # return render_template('municipality.html', municipality=municipality)
    return render_template('municipality.html', municipality=municipality, pagination=pagination, boards=boards)


# @cache.cached(timeout=50)
def view_boards():
    page = request.args.get('page', 1, type=int)
    pagination = OfficialNoticeBoard.query \
        .join(Municipality, OfficialNoticeBoard.ico == Municipality.ico) \
        .paginate(page, per_page=PAGE_SIZE)
    # records = [record.table_dict for record in pagination.items]
    records = [filter_model_to_table(record) for record in pagination.items]
    # titles = [(key, key) for key in OfficialNoticeBoard.__website_columns__]
    titles = map_table_key_names(OfficialNoticeBoard)
    table_name = translate(DEFAULT_LANGUAGE, 'official notice boards', capitalize_mode=2)
    return render_template('boards.html', pagination=pagination, records=records, titles=titles, table_name=table_name, OfficialNoticeBoard=OfficialNoticeBoard)


def view_board(board_id: int):
    board = OfficialNoticeBoard.query.filter(OfficialNoticeBoard.id == board_id).first()

    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.filter(Notice.board_id == board_id).paginate(page, per_page=SUB_PAGE_SIZE)
    notices = pagination.items

    notice_table_name = translate(DEFAULT_LANGUAGE, 'notices', capitalize_mode=2)
    return render_template('board.html', board=board, notice_table_name=notice_table_name, pagination=pagination, notices=notices)


def view_notices():
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.paginate(page, per_page=PAGE_SIZE)
    # records = pagination.items

    records = [filter_model_to_table(record) for record in pagination.items]
    titles = map_table_key_names(Notice)

    table_name = translate(DEFAULT_LANGUAGE, 'notices', capitalize_mode=2)
    return render_template('notices.html', pagination=pagination, records=records, titles=titles, table_name=table_name)


def view_documents():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    if search is None or len(search) == 0:
        pagination = NoticeDocument.query.paginate(page, per_page=PAGE_SIZE)
    else:
        pagination = NoticeDocument.query.filter(NoticeDocument.__ts_vector__.match(search)).paginate(page, per_page=PAGE_SIZE)
    # records = pagination.items

    records = [filter_model_to_table(record) for record in pagination.items]
    titles = map_table_key_names(NoticeDocument)

    table_name = translate(DEFAULT_LANGUAGE, 'documents', capitalize_mode=2)
    return render_template('documents.html', pagination=pagination, records=records, titles=titles, table_name=table_name)
