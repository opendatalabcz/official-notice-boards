from flask import render_template, request

from src.models import *


def index():
    return render_template('index.html')


def municipality():
    page = request.args.get('page', 1, type=int)
    pagination = Municipality.query.paginate(page, per_page=100)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Municipalities')


def board():
    page = request.args.get('page', 1, type=int)
    pagination = OfficialNoticeBoard.query \
        .join(Mapper, OfficialNoticeBoard.ico == Mapper.ico) \
        .join(Municipality, Mapper.ruian == Municipality.ruian) \
        .paginate(page, per_page=100)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Official Notice Boards')


def notice():
    page = request.args.get('page', 1, type=int)
    pagination = Notice.query.paginate(page, per_page=100)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Notice')


def document():
    page = request.args.get('page', 1, type=int)
    pagination = NoticeDocument.query.paginate(page, per_page=100)
    records = pagination.items
    return render_template('table_viewer.html', pagination=pagination, records=records, table_name='Notice Documents')