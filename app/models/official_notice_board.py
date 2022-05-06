from flask import current_app

from app import db
from app.models import Notice
from app.sparql.official_notice_board import fetch_board
from app.utils.random_stuff import return_null_if_empty, nested_get


class OfficialNoticeBoard(db.Model):
    # __website_columns__ = ['id', 'office_name', 'ico']
    __website_columns__ = ['id', 'office_name', 'ico', 'download_url', 'download_url_unreachable']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=True)
    office_name = db.Column(db.String(100), unique=False, nullable=True)
    office_name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    ico = db.Column(db.Integer, unique=False, nullable=True)
    ico_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    municipality_ruian = db.Column(db.Integer, db.ForeignKey('municipality.ruian'), nullable=True)

    download_url = db.Column(db.String(255), unique=False, nullable=True)  # 2083
    download_url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    download_url_unreachable = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    attempted_download = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    notices = db.relationship('Notice', backref='official_notice_board', lazy=True)
    notices_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return f"<OfficialNoticeBoard(id={self.id}, name='{self.office_name}', " \
               f"ico={self.ico}, download_url=' {self.download_url} ')>"

    @classmethod
    def extract_from_dict(cls, data):
        instance = cls()

        # extract office name
        instance.office_name = return_null_if_empty(nested_get(data, ['office_name', 'value']))
        if instance.office_name is None:
            instance.office_name_missing = True

        # extract office ico  # TODO modify SPARQL query to make ICO optional
        instance.ico = return_null_if_empty(nested_get(data, ['ico', 'value']))
        if instance.ico is None:
            instance.ico_missing = True

        instance.name = return_null_if_empty(nested_get(data, ['title', 'value']))

        # extract download url
        download_link = nested_get(data, ['download_link', 'value'])
        if download_link is not None:
            instance.download_url = download_link
        else:
            access_link = nested_get(data, ['access_link', 'value'])
            if access_link is not None:
                instance.download_url = access_link

        if instance.download_url is None:
            instance.download_url_missing = True

        return instance

    def download(self, force_re_download=False) -> bool:
        if self.attempted_download and not force_re_download:
            return True
        self.attempted_download = True

        if self.download_url_missing:
            return False

        fetched_board = fetch_board(self.download_url)
        if fetched_board is None:
            self.download_url_unreachable = True
            return False

        new_notices: list[Notice] = []  # [Notice.extract_from_dict(n) for n in fetched_board]

        for notice_raw in fetched_board:
            new_notice = Notice.extract_from_dict(notice_raw)
            # TODO when different revision, run diff on documents. But this is probably not that common, so wont implement
            existing_notices = Notice.query\
                .filter(Notice.iri == new_notice.iri)\
                .filter(Notice.name == new_notice.name)\
                .filter(Notice.reference_number == new_notice.reference_number)\
                .filter(Notice.revision == new_notice.revision)\
                .order_by(Notice.id)\
                .all()
            if len(existing_notices) > 0:
                if len(existing_notices) > 1:
                    current_app.logger.error("Multiple existing identical notices found, name='%s', iri=%s", new_notice.name, new_notice.iri)
                existing_notice = existing_notices[0]
                # if existing_notice.revision == new_notice.revision
                new_notice.documents = existing_notice.documents
                existing_notice.documents = []

            new_notices.append(new_notice)

        for old_notice in self.notices:
            db.session.delete(old_notice)

        self.notices = new_notices
        for notice_record in self.notices:
            db.session.add(notice_record)

        if len(self.notices) == 0:
            self.notices_missing = True
        return True
