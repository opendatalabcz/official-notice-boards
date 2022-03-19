import docx2txt

from src.text_parsers.parser import Parser


class Docx(Parser):
    @staticmethod
    def parse(file_path: str) -> str | None:
        # try:
        extracted_text = docx2txt.process(file_path)
        # except (IndexError, PSSyntaxError):
        #     extracted_text = None
        return extracted_text
