import os

import pytest

from src.utils.validators.xml_validator import XmlValidator

DATA_DIR_PATH = "utils/validators/data"


def convert_to_full_path(file_name: str) -> str:
    return os.path.join(DATA_DIR_PATH, file_name)


@pytest.mark.parametrize(
    "file_name",
    (
        "valid_xml.xml",
    ),
)
def test_validate_success(file_name: str) -> None:
    assert XmlValidator.validate(convert_to_full_path(file_name))


@pytest.mark.parametrize(
    "file_name",
    (
        "valid_json.json",
        "invalid_file_path.json",
        "invalid_xml_case_mismatch.xml",
        "invalid_xml_more_root_ends.xml",
        "invalid_xml_tag_started_not_ended.xml",
        "invalid_xml_with_incorrect_tag_end_order.xml",
    )
)
def test_validate_fail(file_name: str) -> None:
    assert not XmlValidator.validate(convert_to_full_path(file_name))
