from typing import Optional

from src.app import db


class OfficialNoticeBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String(100), unique=False, nullable=False)
    # municipality
    ico = db.Column(db.Integer, unique=False, nullable=False)
    download_url = db.Column(db.String(255), unique=False, nullable=False)  # 2083

    notices = db.relationship('Notice', backref='official_notice_board', lazy=True)

    def __repr__(self):
        return f"<OfficialNoticeBoard(id={self.id}, name='{self.office_name}', " \
               f"ico={self.ico}, download_url='{self.download_url}')>"

    @classmethod
    def extract_from_dict(cls, data):
        office_name = data['office_name']['value']
        ico = data['ico']['value']
        download_url: Optional[str] = None
        if 'download_link' in data:
            download_url = data['download_link']['value']
        elif 'access_link' in data:
            download_url = data['access_link']['value']
        return cls(office_name=office_name, ico=ico, download_url=download_url)
