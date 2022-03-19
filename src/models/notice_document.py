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
from src.utils.random_stuff import return_null_if_empty, nested_get


class NoticeDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id'), nullable=False)

    name = db.Column(db.String(1024), unique=False, nullable=True)
    name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    download_url = db.Column(db.String(1024), unique=False, nullable=True)  # not required
    download_url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    attempted_download = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    download_url_unreachable = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    downloaded_file_path = db.Column(db.String(255), unique=False, nullable=True)

    file_extension = db.Column(db.String(10), unique=False, nullable=True)
    file_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)  # TODO when file extention == .html?
    attempted_extraction = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    extraction_fail = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    extracted_text = db.Column(db.Text, unique=False, nullable=True)
    file_contains_no_text = db.Column(db.Boolean, unique=False, nullable=False, default=False) # jpeg, xls, ...
    #scanned_document = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    # metric = db.relationship('NoticeDocumentMetric', uselist=False, backref='notice', lazy=True)

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
        new_instance = cls()

        # extract download_url
        new_instance.download_url = return_null_if_empty(data.get('url'))
        if new_instance.download_url is None:
            new_instance.download_url_missing = True

        # extract name
        new_instance.name = return_null_if_empty(nested_get(data, ['název', 'cs']))
        if new_instance.name is None:
            new_instance.name_missing = True

        return new_instance

    def download(self, directory_path: str, force_re_download: bool = False) -> bool:
        if self.download_url_missing:
            logging.info('Missing download url for document with id: %d', self.id)
            return False
        if self.attempted_download and not force_re_download:
            logging.info('Skipping downloading document from %s', self.download_url)
            return True
        self.attempted_download = True

        file_path = os.path.join(directory_path, f"document_id_{self.id}")

        # skip download if file already exists  # TODO delete
        # if os.path.isfile(file_path):
        #     logging.info(f'File {file_path} already exists, skipping download')
        #     print(f'File {file_path} already exists, skipping download')
        #     return True

        # download document
        logging.info('Downloading document from %s to %s', self.download_url, file_path)
        response = requests_wrapper.get(self.download_url)
        if response is None:
            self.download_url_unreachable = True
            return False

        # save document into file
        with open(file_path, 'wb') as doc_file:
            for chunk in response.iter_content(chunk_size=1024):
                doc_file.write(chunk)
        self.downloaded_file_path = file_path

        self.file_extension = requests_wrapper.extract_file_name_extension_from_response(response)
        return True

    def extract_text(self, force_re_extract: bool = False) -> bool:
        if self.downloaded_file_path is None:
            return False
        if self.attempted_extraction and not force_re_extract:
            return True
        self.attempted_extraction = True

        # gets parser for given file extension
        parser = get_parser(self.file_extension)
        if parser is None:
            logging.info('Skipping text extraction from %s with extension %s', self.downloaded_file_path, self.file_extension)
            self.extraction_fail = True
            return False

        # attempts to extract text from file
        logging.info('Extracting text from %s', self.downloaded_file_path)
        try:
            self.extracted_text = parser.parse(self.downloaded_file_path)
        except Exception:
            self.extraction_fail = True
            return False

        # Check if text is empty
        if self.extracted_text is None:
            self.file_contains_no_text = True
        return True
