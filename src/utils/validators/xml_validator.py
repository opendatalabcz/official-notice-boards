from xml.etree import ElementTree

from src.utils.validators.file_validator import FileValidator


class XmlValidator(FileValidator):
    @classmethod
    def validate(cls, file_path) -> bool:
        if not cls.check_file_path(file_path):
            return False

        with open(file_path, 'r') as f:
            try:
                ElementTree.fromstring(f.read())
            except ElementTree.ParseError:
                return False
            return True
