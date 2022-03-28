from pdfminer.high_level import extract_text
from pdfminer.psparser import PSSyntaxError

from app.text_parsers.parser import Parser


class PDF(Parser):
    @staticmethod
    def parse(file_path: str) -> str | None:
        # try:
        extracted_text = extract_text(file_path)
        # except (IndexError, PSSyntaxError):
        #     extracted_text = None
        # if extracted_text == "":
        # TODO try OCR
        return extracted_text
