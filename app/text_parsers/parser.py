from abc import ABC, abstractmethod


class Parser(ABC):
    @staticmethod
    @abstractmethod
    def parse(file_path) -> str | None:
        return None
        # raise NotImplementedError
