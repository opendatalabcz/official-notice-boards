import os

import pytest

from src.utils.validators.json_validator import JsonValidator

DATA_DIR_PATH = "unit/utils/validators/data"


def convert_to_full_path(file_name: str) -> str:
    return os.path.join(DATA_DIR_PATH, file_name)


@pytest.mark.parametrize(
    "file_name",
    (
        "valid_json.json",
        "valid_empty_json.json",
    ),
)
def test_validate_success(file_name: str) -> None:
    assert JsonValidator.validate(convert_to_full_path(file_name))


@pytest.mark.parametrize(
    "file_name",
    (
        "valid_xml.xml",
        "invalid_file_path.json",
        "invalid_json_missing_ending_curly_brace.json",
        "invalid_json_string_not_ended_brace.json",
        # "utils/validators/data/valid_json.xml",
    )
)
def test_validate_fail(file_name: str) -> None:
    assert not JsonValidator.validate(convert_to_full_path(file_name))
