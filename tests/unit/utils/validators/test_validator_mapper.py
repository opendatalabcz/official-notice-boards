from typing import Type

import pytest

from src.utils.validators.file_type import FileType
from src.utils.validators import validator_mapper
from src.utils.validators.file_validator import FileValidator
from src.utils.validators.json_validator import JsonValidator
from src.utils.validators.xml_validator import XmlValidator


@pytest.mark.parametrize(
    "file_type, validator",
    (
        (
            FileType.JSON,
            JsonValidator
        ),
    ),
)
def test_get_validator(file_type: FileType, validator: Type[FileValidator]) -> None:
    assert validator_mapper.get_validator(file_type) is validator


@pytest.mark.parametrize(
    "file_type, validator",
    (
        (
            FileType.CSV,
            XmlValidator
        ),
    ),
)
def test_get_validator_negative(file_type: FileType, validator: Type[FileValidator]) -> None:
    assert validator_mapper.get_validator(file_type) is not validator
