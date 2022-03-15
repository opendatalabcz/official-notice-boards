from datetime import datetime
from typing import Optional

from src.app import db
# from src.models import *
from src.models.notice_document import NoticeDocument


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iri = db.Column(db.String(1024), unique=False, nullable=True)
    # url = db.Column(db.String(1024), unique=False, nullable=True)  # TODO uncomment
    # types: list[Type]
    name = db.Column(db.Text, unique=False, nullable=True)  # TODO change, db.String(2048), either really too short, or some weird character is causing trouble
    post_date = db.Column(db.DateTime, unique=False, nullable=True)
    relevant_until = db.Column(db.DateTime, unique=False, nullable=True)
    # agendas : list[Agenda]
    documents = db.relationship('NoticeDocument', backref='notice', lazy=True)
    board_id = db.Column(db.Integer, db.ForeignKey('official_notice_board.id'), nullable=True)

    def __repr__(self):
        return f"<Notice(id={self.id}, name='{self.name}', " \
               f"iri='{self.iri}', documents={self.documents})>"
               # f"iri='{self.iri}', url='{self.url}', documents={self.documents})>"

    @staticmethod
    def _extract_datetime_from_dict(data) -> Optional[datetime]:
        match data:
            case None | {"nespecifikovaný": True} | {"datum": "" | "0000-00-00" | "-"}:  # TODO move under default case
                date = None  # datetime.utcnow()
            case {"datum": date_raw}:
                date = datetime.fromisoformat(date_raw)
            case {"datum_a_čas": date_raw} | {"Časový okamžik": date_raw}:  # TODO mark as not spec compliant
                date = datetime.fromisoformat(date_raw)
            case _:
                # raise ValueError(f"Unknown datetime format: {data}")
                date = None
        return date

    @classmethod
    def extract_from_dict(cls, data):
        iri = data.get('iri')  # Required in spec, but usually not present
        # url = data.get('url')
        name = data.get('název', {}).get('cs')

        post_date_raw = data.get('vyvěšení')
        post_date = cls._extract_datetime_from_dict(post_date_raw)

        relevant_until_raw = data.get('relevantní_do')
        relevant_until = cls._extract_datetime_from_dict(relevant_until_raw)

        documents: list[NoticeDocument] = []
        documents_raw = data.get('dokument', [])
        match documents_raw:
            case None | []:
                # download_url = None
                print(f"Warning: no documents for {iri}")
            case [document_raw]:
                document = NoticeDocument.extract_from_dict(document_raw)
                db.session.add(document)  # TODO move elsewhere, maybe not necessary
                documents.append(document)
            case [_, *_]: # TODO combine with previous case
                documents: list[NoticeDocument] = []
                for document_raw in documents_raw:
                    document = NoticeDocument.extract_from_dict(document_raw)
                    db.session.add(document)  # TODO move elsewhere, maybe not necessary
                    documents.append(document)
            case _:
                raise ValueError(f"Unknown documents format: {documents_raw}")

        return cls(iri=iri, name=name, post_date=post_date,
                   relevant_until=relevant_until, documents=documents)
