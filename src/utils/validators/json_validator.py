import json

from src.utils.validators.file_validator import FileValidator


class JsonValidator(FileValidator):
    @classmethod
    def validate(cls, file_path) -> bool:
        if not cls.check_file_path(file_path):
            return False

        with open(file_path, 'r') as file:
            try:
                json.load(file)
            except json.decoder.JSONDecodeError:
                return False
            return True
