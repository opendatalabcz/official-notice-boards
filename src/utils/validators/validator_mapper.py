from typing import Type, Iterator

from src.utils.validators.csv_validator import CsvValidator
from src.utils.validators.file_type import FileType
from src.utils.validators.file_validator import FileValidator
from src.utils.validators.json_validator import JsonValidator
from src.utils.validators.jsonld_validator import JsonLdValidator
from src.utils.validators.xml_validator import XmlValidator

_MAPPER: dict[FileType, Type[FileValidator]] = {
    FileType.CSV: CsvValidator,
    FileType.JSON: JsonValidator,
    FileType.JSON_LD: JsonLdValidator,
    FileType.XML: XmlValidator,

}


def get_validator(file_type: FileType) -> Type[FileValidator]:
    return _MAPPER[file_type]


def get_all_validators() -> Iterator[tuple[FileType, Type[FileValidator]]]:
    return iter(_MAPPER.items())  # TODO fix type annotation or value
