from typing import Optional, Type

from src.text_parsers.parser import Parser
from src.text_parsers.pdf import PDF

mapper = {
    'pdf': PDF
    # 'docx': Parser,
    # 'xlsx': Parser,  # Can probably be ignored
    # 'doc': Parser,
    # 'xls': Parser,
    # 'sheet': Parser,  # Can probably be ignored  # TODO check, probably is xlxs
    # 'jpg': Parser,  # Can probably be ignored
    # 'png': Parser,  # Can probably be ignored
    # 'jpeg': Parser,  # Can probably be ignored
    # 'odt': Parser,
    # 'zip': Parser,  # unzip -> many documents
    # 'html': Parser,  # ignore, permission denied
    # 'rtf': Parser,
}


def get_parser(file_extension: str) -> Type[Parser] | None:
    return mapper.get(file_extension)
    # return mapper.get(file_extension, Parser)
