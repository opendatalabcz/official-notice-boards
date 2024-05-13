import logging
import re

import requests


def get(url: str, headers=None, params=None, timeout=None) -> requests.Response | None:
    """
    Wrapper for requests.get() with additional checks
    """
    if url is None or url == '':
        logging.debug("Invalid url when sending GET request to %s", url)
        return None

    if headers is None:
        headers = {}
    if params is None:
        params = {}
    # this neste try except, because inside the first except SSLError block, the new request can also throw SSLError
    try:
        try:
            logging.debug("Sending GET request to %s", url)
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
        except requests.exceptions.SSLError:
            logging.debug("RE-sending GET request without SSL certificate verification to %s", url)
            response = requests.get(url, headers=headers, params=params, timeout=timeout, verify=False)  # TODO False should be replace by path to certificate, this might be a security risk, not sure if it should be in final version. Also this option could be called directly, which would make it run faster
    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError):
        logging.debug("Connection error when sending GET request to %s", url)
        response = None
    except Exception as e:
        logging.warning("Error (%s) when sending GET request to %s", e, url)
        response = None
    return response


def extract_file_name_from_response(response: requests.Response) -> str:
    document_name = response.headers.get('Content-filename')
    # if document_name is not None:
    #     return document_name
    #
    # content_disposition = response.headers.get('Content-Disposition')
    # if content_disposition is not None:
    #     document_name = re.findall("filename=(.+)", content_disposition)[0]
    #
    # if document_name is not None:
    #     return document_name
    #
    # content_type = response.headers.get('Content-Type')
    # if content_type is not None:
    #     document_name = '.' + content_type.split('/')[-1]
    #
    # if document_name is not None:
    #     return document_name
    #
    # return response.url.split('/')[-1]

    if document_name is None:  # TODO replace by commented part, but be careful, test it first
        if content_disposition := response.headers.get('Content-Disposition'):
            if filenames := re.findall("filename=(.+)", content_disposition):
                return filenames[0]
    if document_name is None:
        content_type = response.headers.get('Content-Type')
        if content_type:
            document_name = '.' + content_type.split('/')[-1]
    if document_name is None:
        document_name = response.url.split('/')[-1]

    return document_name


def extract_file_name_extension_from_response(response: requests.Response) -> str:
    document_name = extract_file_name_from_response(response)
    file_extension = document_name.rsplit('.', maxsplit=1)[-1]
    file_extension = file_extension.split(';', maxsplit=1)[0]
    if len(file_extension) > 10:
        file_extension = file_extension[:10]
    return file_extension.replace('"', '').lower()
