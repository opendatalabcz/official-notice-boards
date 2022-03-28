from app.text_parsers.parser import Parser


class NoText(Parser):
    @staticmethod
    def parse(file_path) -> str | None:
        return None
