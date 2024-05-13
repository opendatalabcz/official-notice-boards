from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    TESTING = False
    FLASK_DEBUG = False
    DEVELOPMENT = False

    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_BOOTSWATCH_THEME = 'Cosmo'

    IMPORT_ONLY_MUNICIPALITY_BOARDS = environ.get('IMPORT_ONLY_MUNICIPALITY_BOARDS', False)
    DOWNLOADED_DOCUMENT_DIRECTORY = environ.get('DOWNLOADED_DOCUMENT_DIRECTORY', './data/documents')
    DELETE_DOCUMENTS_AFTER_EXTRACTION = environ.get('DELETE_DOCUMENTS_AFTER_EXTRACTION', True)

    LOGGING_LEVEL = environ.get('LOGGING_LEVEL', 'INFO')
