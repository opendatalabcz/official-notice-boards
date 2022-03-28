from flask import render_template, request
from sqlalchemy import func

from app.language_translations import translate
from app.models import *

PAGE_SIZE = 100
SUB_PAGE_SIZE = 10
DEFAULT_LANGUAGE = 'cs'  # TODO move elsewhere


def index():
    return render_template('index.html')


def view_municipalities():
    page = request.args.get('page', 1, type=int)
    pagination = Municipality.query.paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    table_name = translate(DEFAULT_LANGUAGE, 'municipalities', capitalize_mode=2)
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name=table_name)


# @cache.cached(timeout=50)
def view_boards():
    page = request.args.get('page', 1, type=int)
    pagination = OfficialNoticeBoard.query \
        .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
        .join(Municipality, Mapper.ruian == Municipality.ruian) \
        .paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    table_name = translate(DEFAULT_LANGUAGE, 'official notice boards', capitalize_mode=2)
    return render_template('boards.html', pagination=pagination, records=records, table_name=table_name, OfficialNoticeBoard=OfficialNoticeBoard)


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
    records = pagination.items
    table_name = translate(DEFAULT_LANGUAGE, 'notices', capitalize_mode=2)
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name=table_name)


def view_documents():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    if search is None or len(search) == 0:
        pagination = NoticeDocument.query.paginate(page, per_page=PAGE_SIZE)
    else:
        pagination = NoticeDocument.query.filter(NoticeDocument.__ts_vector__.match(search)).paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    table_name = translate(DEFAULT_LANGUAGE, 'documents', capitalize_mode=2)
    return render_template('documents.html', pagination=pagination, records=records, table_name=table_name)
    # return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Notice Documents')


def view_graphs():

    # # get counts of notices per municipality
    # db.session.query(func.count(Notice.id)) \
    #     .select_from(OfficialNoticeBoard)\
    #     .outerjoin(Notice) \
    #     .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
    #     .join(Municipality, Mapper.ruian == Municipality.ruian) \
    #     .group_by(OfficialNoticeBoard.id).all()

    all_boards_count = OfficialNoticeBoard.query.count()
    boards_by_municipalities = OfficialNoticeBoard.query \
        .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
        .join(Municipality, Mapper.ruian == Municipality.ruian) \
        .count()
    boards_rest_count = all_boards_count - boards_by_municipalities

    all_municipality_offices_count = Municipality.query.count()
    municipalities_rest_count = all_municipality_offices_count - boards_by_municipalities

    documents_extensions_query = db.session.query(func.count(NoticeDocument.file_extension).
                           label('total_count'),
                           NoticeDocument.file_extension)\
        .group_by(NoticeDocument.file_extension)\
        .all()
    documents_extensions_query.sort(reverse=True)
    documents_extensions_data, documents_extensions_labels = map(list, zip(*documents_extensions_query))
    documents_extensions_labels = ['None' if x is None else x for x in documents_extensions_labels]

    page_name = translate(DEFAULT_LANGUAGE, 'graphs', capitalize_mode=2)
    return render_template('graph.html',
                           page_name=page_name,
                           boards_by_municipalities=boards_by_municipalities,
                           boards_rest_count=boards_rest_count,
                           municipalities_rest_count=municipalities_rest_count,
                           documents_extensions_data=documents_extensions_data,
                           documents_extensions_labels=documents_extensions_labels)
