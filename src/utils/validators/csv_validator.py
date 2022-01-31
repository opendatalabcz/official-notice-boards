import csv
from xml.etree import ElementTree

from src.utils.validators.file_validator import FileValidator


class CsvValidator(FileValidator):
    @classmethod
    def validate(cls, file_path) -> bool:  # TODO do differently, this does not work properly
        if not cls.check_file_path(file_path):
            return False

        with open(file_path, 'r') as f:
            try:
                csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
            except csv.Error:
                return False
            return True
