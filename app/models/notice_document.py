import logging
import os

from flask import current_app
from sqlalchemy import Index

from app import db
from app.models.tsvector_impl import TSVector
from app.text_parsers.mapper import get_parser
from app.utils import requests_wrapper
from app.utils.random_stuff import return_null_if_empty, nested_get


MIN_TEXT_LENGTH = 50


class NoticeDocument(db.Model):
    __website_columns__ = ['id', 'name', 'download_url', 'file_extension', 'shortened_extracted_text']

    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id'), nullable=False)

    name = db.Column(db.String(1024), unique=False, nullable=True)
    name_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    download_url = db.Column(db.String(1024), unique=False, nullable=True)
    download_url_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    attempted_download = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    download_url_unreachable = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    downloaded_file_path = db.Column(db.String(255), unique=False, nullable=True)

    file_extension = db.Column(db.String(10), unique=False, nullable=True)
    file_missing = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    attempted_extraction = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    extraction_fail = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    extracted_text = db.Column(db.Text, unique=False, nullable=True)
    shortened_extracted_text = db.Column(db.String(100), unique=False, nullable=True)
    file_contains_no_text = db.Column(db.Boolean, unique=False, nullable=False, default=False)  # jpeg, xls, ...

    # # if True:  # change condition, this can be used to allow compatibility with other databases. Find out this could be find out from db instance
    # __ts_vector__ = db.Column(TSVector(), db.Computed(
    #     "to_tsvector('english', name || ' ' || extracted_text)",
    #     persisted=True))
    #
    # __table_args__ = (Index('ix_notice_document___ts_vector__',
    #                         __ts_vector__, postgresql_using='gin'),)

    def __repr__(self):
        return f"<NoticeDocument(id={self.id}, name='{self.name}', download_url='{self.download_url}', " \
               f"downloaded_file_path='{self.downloaded_file_path}', file_extension='{self.file_extension}', " \
               f"extracted_text='{self.extracted_text[:10]+'...' if self.extracted_text is not None else None}'>"

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
        if self.attempted_download and not force_re_download:
            logging.info('Skipping downloading document from %s', self.download_url)
            return True
        self.attempted_download = True

        if self.download_url_missing:
            logging.info('Missing download url for document with id: %d', self.id)
            return False

        file_path = os.path.join(directory_path, f"document_id_{self.id}")

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

        # if file extension is .html, that means the download_url
        # is pointing to a webpage nad not a file, or the url is invalid
        if self.file_extension == 'html':
            logging.info('Skipping extraction of html file')
            self.file_contains_no_text = True
            return False

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
            if self.extracted_text is not None:
                self.extracted_text = self.extracted_text.replace("\x00", "\uFFFD")
        except Exception as e:
            self.extraction_fail = True
            current_app.logger.warn(f'Extraction of document {self} failed with exception {e}', exc_info=True)
            return False

        # TODO if empty and pdf, try OCR
        #  check https://stackoverflow.com/questions/63983531/use-tesseract-ocr-to-extract-text-from-a-scanned-pdf-folders

        # Check if text is empty
        if self.extracted_text is None or len(self.extracted_text) < MIN_TEXT_LENGTH:
            self.file_contains_no_text = True
        else:
            # stripped_short_text = self.extracted_text[:MIN_TEXT_LENGTH].strip()
            self.shortened_extracted_text = self.extracted_text[:97].strip() + '...'
        return True

    def delete_file(self):
        if self.downloaded_file_path is not None:
            os.remove(self.downloaded_file_path)
            self.downloaded_file_path = None
