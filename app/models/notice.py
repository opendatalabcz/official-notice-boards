import logging
from datetime import datetime

from app import db
# from src.models import *
from app.models.notice_document import NoticeDocument
from app.utils.random_stuff import return_null_if_empty, nested_get


class Notice(db.Model):
    __website_columns__ = ['id', 'name', 'url', 'post_date']

    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('official_notice_board.id'), nullable=True)

    iri = db.Column(db.String(1024), unique=False, nullable=True)
    iri_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    url = db.Column(db.String(1024), unique=False, nullable=True)
    url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    name = db.Column(db.Text, unique=False, nullable=True)
    name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    description = db.Column(db.Text, unique=False, nullable=True)
    description_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    reference_number = db.Column(db.String(255), unique=False, nullable=True)
    reference_number_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    revision = db.Column(db.String(100), unique=False, nullable=True)

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
                try:
                    date = datetime.fromisoformat(date_raw)  # TODO wrap by try/except
                    bad_format = False
                except ValueError:
                    logging.warning("Wrong date format: %s", data)
            case {"Časový okamžik": date_raw}:
                date = datetime.fromisoformat(date_raw)
            case _:
                logging.warning("Wrong date format: %s", data)
        return date, bad_format

    @classmethod
    def extract_from_dict(cls, data):
        instance = cls()

        # extract IRI
        instance.iri = return_null_if_empty(data.get('iri'))
        instance.iri_missing = bool(instance.iri is None)

        # extract URL
        instance.url = return_null_if_empty(data.get('url'))
        instance.url_missing = bool(instance.url is None)

        # extract name
        instance.name = return_null_if_empty(nested_get(data, ['název', 'cs']))
        instance.name_missing = bool(instance.name is None)

        # extract description
        instance.description = return_null_if_empty(nested_get(data, ['popis', 'cs']))
        instance.description_missing = bool(instance.description is None)

        # extract reference_number
        instance.reference_number = return_null_if_empty(data.get('číslo_jednací'))
        instance.reference_number_missing = bool(instance.reference_number is None)

        instance.revision = data.get('revize')


        # extract dates
        instance.post_date, instance.post_date_wrong_format = \
            cls._extract_datetime_from_dict(data.get('vyvěšení'))
        instance.relevant_until_date, instance.relevant_until_date_wrong_format = \
            cls._extract_datetime_from_dict(data.get('relevantní_do'))

        # extract documents (only info about it)
        documents_raw = data.get('dokument', [])
        match documents_raw:
            case None | []:
                instance.documents_missing = True
                logging.info("No documents for %s}", instance.url)
            case [_] | [_, *_]:
                for document_raw in documents_raw:
                    instance.documents.append(NoticeDocument.extract_from_dict(document_raw))
            case _:
                instance.documents_wrong_format = True
                logging.warning("Wrong documents format for %s: %s", instance.url, documents_raw)
        return instance
