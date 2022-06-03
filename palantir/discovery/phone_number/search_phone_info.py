import urllib.request
import json
from typing import NamedTuple

from palantir.discovery.phone_number import exceptions


class PhoneInfo(NamedTuple):
    country: str
    okrug: str
    region: str
    time_zone: str
    oper_brand: str


def search_phone(phone: str) -> PhoneInfo:
    url = "https://htmlweb.ru/geo/api.php?json&telcod=" + phone
    try:
        phone_info = urllib.request.urlopen(url)
        phone_info_json = json.load(phone_info)

        return PhoneInfo(
            phone_info_json['fullname'],
            phone_info_json['okrug'],
            phone_info_json['region']['name'],
            phone_info_json['tz'],
            phone_info_json['0']['oper_brand'],
        )
    except Exception as e:
        raise exceptions.PhoneError(f'PhoneError')


# if __name__ == "__main__":
#     phone_info = search_phone('79528813602')
#     for info in phone_info:
#         print(f'{info}')
