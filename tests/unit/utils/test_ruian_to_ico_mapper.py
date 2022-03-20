from unittest import mock
# from pytestmock import mock
# from pytest_mock import MockerFixture
# import mock
import pytest

from src.app import db
from src.models import Mapper


# @pytest.fixture(scope='module')
# def mapper():
#     db.create_all()
#     m = RuianToIcoMapper()  # TODO mock SparqlWrapper
#     m.update_mapper_info()
#     return m

@pytest.mark.skip(reason="will have to download data")
def test_get_ico_municipality():
    assert 265209 == Mapper.get_ico(565971)
    # assert '00265209' == mapper.get_ico('565971')

@pytest.mark.skip(reason="will have to download data")
def test_get_ico_municipality_part_prague():
    assert 231151 == Mapper.get_ico(547107)
    # assert '00231151' == mapper.get_ico('547107')


@pytest.mark.skip(reason="Currently not supported")
def test_get_ico_municipality_part_else():
    assert 99999999 == Mapper.get_ico(554570)
    # assert "99999999" == mapper.get_ico('554570')

@pytest.mark.skip(reason="will have to download data")
def test_get_ico_fail():
    assert Mapper.get_ico(999999) is None
    # assert mapper.get_ico('999999') is None

#
# @mock.patch(SPARQLWrapper)
# def test_get_ico_municipality_mocked():
#     SPARQLWrapper
#     assert '00265209' == mapper.get_ico('565971')
