import logging
import os
import re
from typing import Optional, Type

import flask_whooshalchemy3
from sqlalchemy import Index
from whoosh.analysis import StemmingAnalyzer

from src import text_parsers
from src.app import db
from src.models.tsvector_impl import TSVector
from src.text_parsers.mapper import get_parser
from src.text_parsers.parser import Parser
from src.utils import requests_wrapper


class NoticeDocument(db.Model):
    # __tablename__ = 'notice_document'
    # __searchable__ = ['name', 'extracted_text']  # indexed fields
    # __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=False, nullable=True)
    download_url = db.Column(db.String(1024), unique=False, nullable=True)  # not required
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id'), nullable=False)
    downloaded_file_path = db.Column(db.String(255), unique=False, nullable=True)
    file_extension = db.Column(db.String(10), unique=False, nullable=True)
    extracted_text = db.Column(db.Text, unique=False, nullable=True)

    __ts_vector__ = db.Column(TSVector(), db.Computed(
        "to_tsvector('english', name || ' ' || extracted_text)",
        persisted=True))

    __table_args__ = (Index('ix_notice_document___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)

    def __repr__(self):
        return f"<NoticeDocument(id={self.id}, name='{self.name}', download_url='{self.download_url}', " \
               f"downloaded_file_path='{self.downloaded_file_path}', file_extension='{self.file_extension}', " \
               f"extracted_text='{self.extracted_text[:10]+'...' if self.extracted_text is not None else None}'>"
               # f"len(extracted_text)={len(self.extracted_text)}>"

    @classmethod
    def full_text_search(cls, query: str) -> list:
        return cls.query.filter(cls.__ts_vector__.match(query)).all()

    @classmethod
    def extract_from_dict(cls, data):
        download_url: Optional[str] = data.get('url')
        if download_url == '':
            download_url = None
        name = data.get('název', {}).get('cs')
        return cls(name=name, download_url=download_url)

    def download(self, directory_path) -> bool:
        response = requests_wrapper.get(self.download_url)
        if response is None:
            return False

        file_name = f"document_id_{self.id}"
        file_path = os.path.join(directory_path, file_name)

        # skip download if file already exists
        if os.path.isfile(file_path):
            logging.info(f'File {file_path} already exists, skipping download')
            print(f'File {file_path} already exists, skipping download')
            return True

        # download document
        logging.info('Downloading document from %s to %s', self.download_url, file_path)
        with open(file_path, 'wb') as doc_file:
            for chunk in response.iter_content(chunk_size=1024):
                doc_file.write(chunk)
        self.downloaded_file_path = file_path

        self.file_extension = requests_wrapper.extract_file_name_extension_from_response(response)
        return True

    def delete_file(self) -> bool:
        if self.downloaded_file_path is None:
            logging.info('Cannot delete file with NULL path')
            return False
        if not os.path.isfile(self.downloaded_file_path):
            logging.info('Cannot delete file, because it does not exist')
            return False
        logging.info(f'Deleting file {self.downloaded_file_path}')
        os.remove(self.downloaded_file_path)
        return True

    def extract_text(self):  # TODO add support for other formats than PDF,
        if self.downloaded_file_path is None:
            return
        # if self.downloaded_file_path.endswith('.pdf'):
        logging.info(f'Extracting text from %s', self.downloaded_file_path)
        print(f'Extracting text from {self.downloaded_file_path}')
        # self.extracted_text = extract_text(self.downloaded_file_path)
        parser: Type[Parser] | None = get_parser(self.file_extension)
        if parser is not None:
            self.extracted_text = parser.parse(self.downloaded_file_path)

# whoosh_index(app, NoticeDocument)