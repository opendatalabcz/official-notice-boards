from app import db
from app.models import Notice
from app.sparql.official_notice_board import fetch_board
from app.utils.random_stuff import return_null_if_empty, nested_get


class OfficialNoticeBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String(100), unique=False, nullable=True)
    office_name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    # municipality
    ico = db.Column(db.Integer, unique=False, nullable=True)
    ico_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    download_url = db.Column(db.String(255), unique=False, nullable=True)  # 2083
    download_url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    download_url_unreachable = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    attempted_download = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    notices = db.relationship('Notice', backref='official_notice_board', lazy=True)
    notices_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return f"<OfficialNoticeBoard(id={self.id}, name='{self.office_name}', " \
               f"ico={self.ico}, download_url='{self.download_url}')>"

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

        fetched_boards = fetch_board(self.download_url)
        if fetched_boards is None:
            self.download_url_unreachable = True
            return False

        for notice_raw in fetched_boards:
            notice_record = Notice.extract_from_dict(notice_raw)
            self.notices.append(notice_record)

        if len(self.notices) == 0:
            self.notices_missing = True
        return True
