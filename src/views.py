from flask import render_template, request
from sqlalchemy import func

from src.models import *

PAGE_SIZE = 100

def index():
    return render_template('index.html')


def municipality():
    page = request.args.get('page', 1, type=int)
    pagination = Municipality.query.paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Municipalities')


def board():
    page = request.args.get('page', 1, type=int)
    pagination = OfficialNoticeBoard.query \
        .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
        .join(Municipality, Mapper.ruian == Municipality.ruian) \
        .paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Official Notice Boards')


def notice():
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.paginate(page, per_page=PAGE_SIZE)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Notice')


def document():
    page = request.args.get('page', 1, type=int)
    pagination = NoticeDocument.query.paginate(page, per_page=100)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Notice Documents')


def graph():

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

    return render_template('graph.html',
                           boards_by_municipalities=boards_by_municipalities,
                           boards_rest_count=boards_rest_count,
                           municipalities_rest_count=municipalities_rest_count,
                           documents_extensions_data=documents_extensions_data,
                           documents_extensions_labels=documents_extensions_labels
                           )