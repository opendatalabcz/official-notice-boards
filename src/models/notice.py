import logging
from datetime import datetime
from typing import Optional

from src.app import db
# from src.models import *
from src.models.notice_document import NoticeDocument
from src.utils.random_stuff import return_null_if_empty, nested_get


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('official_notice_board.id'), nullable=True)

    iri = db.Column(db.String(1024), unique=False, nullable=True)
    iri_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    url = db.Column(db.String(1024), unique=False, nullable=True)  # TODO uncomment
    url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    # types: list[Type]
    name = db.Column(db.Text, unique=False, nullable=True)  # TODO change, db.String(2048), either really too short, or some weird character is causing trouble
    name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    post_date = db.Column(db.DateTime, unique=False, nullable=True)
    post_date_wrong_format = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    relevant_until_date = db.Column(db.DateTime, unique=False, nullable=True)
    relevant_until_date_wrong_format = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    # agendas : list[Agenda]
    documents = db.relationship('NoticeDocument', backref='notice', lazy=True)
    documents_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    documents_wrong_format = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    def __repr__(self):
        return f"<Notice(id={self.id}, name='{self.name}', iri='{self.iri}', " \
               f"url='{self.url}', documents={self.documents})>"

    @staticmethod
    def _extract_datetime_from_dict(data) -> tuple[datetime | None, bool]:
        """Returns datetime and bool indicating if the datetime has correct format"""
        bad_format = True
        date = None
        match data:
            case None | {"datum": "" | "0000-00-00" | "-" | 'None'}:
                pass
            case {"nespecifikovaný": True}:
                bad_format = False
            case {"datum": date_raw} | {"datum_a_čas": date_raw}:
                date = datetime.fromisoformat(date_raw)  # TODO wrap by try/except
                bad_format = False
            case {"Časový okamžik": date_raw}:  # TODO maybe delete and put in default case
                date = datetime.fromisoformat(date_raw)
            case _:
                pass
        return date, bad_format

    @classmethod
    def extract_from_dict(cls, data):  # TODO check url == '-as4udetail-65481'
        instance = cls()

        # extract IRI
        instance.iri = return_null_if_empty(data.get('iri'))
        if instance.iri is None:
            instance.iri_missing = True

        # extract URL
        instance.url = return_null_if_empty(data.get('url'))
        if instance.url is None:
            instance.url_missing = True

        # extract name
        instance.name = return_null_if_empty(nested_get(data, ['název', 'cs']))
        if instance.name is None:
            instance.name_missing = True

        # extract dates
        instance.post_date, instance.post_date_wrong_format = \
            cls._extract_datetime_from_dict(data.get('vyvěšení'))
        instance.relevant_until_date, instance.relevant_until_date_wrong_format = \
            cls._extract_datetime_from_dict(data.get('relevantní_do'))

        # extract documents
        documents_raw = data.get('dokument', [])
        match documents_raw:
            case None | []:
                instance.documents_missing = True
                logging.info("No documents for %s}", instance.url)
            case [_] | [_, *_]:  # 1+ documents in a list
                for document_raw in documents_raw:
                    instance.documents.append(NoticeDocument.extract_from_dict(document_raw))
            case _:
                instance.documents_wrong_format = True
                logging.info("Wrong documents format for %s: %s", instance.url, documents_raw)
                # raise ValueError(f"Unknown documents format: {documents_raw}")
        return instance
