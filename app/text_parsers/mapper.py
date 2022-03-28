from typing import Optional, Type

from app.text_parsers.docx import Docx
from app.text_parsers.no_text import NoText
from app.text_parsers.parser import Parser
from app.text_parsers.pdf import PDF

mapper = {
    'pdf': PDF,
    'docx': Docx,
    'xlsx': NoText,  # Can probably be ignored
    # 'doc': Parser,
    'xls': NoText,
    'sheet': NoText,  # Can probably be ignored  # TODO check, probably is xlxs
    'jpg': NoText,  # Can probably be ignored
    'png': NoText,  # Can probably be ignored
    'jpeg': NoText,  # Can probably be ignored
    # 'odt': Parser,
    # 'zip': Parser,  # unzip -> many documents
    # 'html': Parser,  # ignore, permission denied
    # 'rtf': Parser,
}


def get_parser(file_extension: str) -> Type[Parser] | None:
    return mapper.get(file_extension)
    # return mapper.get(file_extension, Parser)
