# from datetime import datetime
#
# import pytest
#
# from src.utils.municipality_list_czso_csv import create_url
#
# #
# # @pytest.mark.parametrize(
# #     "raw_datasource",
# #     (
# #             dict(),  # invalid1
# #             {"foo": "bar"},  # invalid2
# #             {"url": "example.com"},  # missing most of attributes
# #             {"url": "", "method": "FOO"},  # wrong HTTP method
# #             {
# #                 "name": "http1",
# #                 "url": "https://google.com",
# #                 "method": "GET",
# #                 "jsonpath": "",  # empty jmespath
# #             },
# #     ),
# # )
# # def test_invalid_httpdatasource(raw_datasource: Mapping[str, Any]) -> None:
# #     with pytest.raises(pydantic.ValidationError):
# #         HTTPDataSource(**raw_datasource)
#
# @pytest.mark.skip(reason="cisvaz is a randomly generated, co cannot be compared")
# @pytest.mark.parametrize(
#     "date, output_url",
#     (
#         # basic
#         (
#                 {
#                     'day': 1,
#                     'month': 1,
#                     'year': 2000
#                 },
#                 "https://apl.czso.cz/iSMS/cisexp.jsp?kodcis=43&typdat=0&cisvaz=42_1218&datpohl=01.01.2000&cisjaz=203&format=2&separator=%2C"
#                 "https://apl.czso.cz/iSMS/cisexp.jsp?kodcis=43&typdat=2&cisvaz=80007_1771&datpohl=01.01.2000&cisjaz=203&format=2&separator=%2C"
#         ),
#         # (([],), [])
#     ),
# )
# def test_create_url_specified_date(date: dict[str, int], output_url: str) -> None:
#     assert create_url(datetime(**date)) == output_url
