import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urlencode

import requests as requests

URL_BASE_MUNICIPALITY_LIST = "https://apl.czso.cz/iSMS/cisexp.jsp?"


def create_url(date: Optional[datetime] = None):

    if date is None:
        date = datetime.now()

    params = {
        'kodcis': '43',
        'typdat': '2',
        'cisvaz': '80007_1771',
        'datpohl': date.strftime("%d.%m.%Y"),
        'cisjaz': '203',  # 203 = czech, 8260 = english
        'format': '2',  # 0 = xml, 1 = DBF, 2 = CSV
        'separator': ','
    }

    return URL_BASE_MUNICIPALITY_LIST + urlencode(params)


def download_municipalities_list():
    url = create_url()
    with requests.Session() as s:
        logging.debug(f"Downloading list of municipalities with target url: {url}")
        response = s.get(url, stream=True)

        with open('tmp/data.csv', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        # decoded_content = response.content.decode('Windows-1250')
        # cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        # for l in cr:
        #     print(l)
