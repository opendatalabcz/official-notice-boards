import os.path
from abc import ABC, abstractmethod


class FileValidator(ABC):  # TODO also check for file extensions
    @staticmethod
    def check_file_path(file_path) -> bool:
        """Checks if the file path is valid"""
        return os.path.isfile(file_path)

    @classmethod
    @abstractmethod
    def validate(cls, file_path) -> bool:  #
        """Checks if the file is of a certain format"""
        raise NotImplementedError

    # TODO add another method to call check_file_path and validate to dedupe code