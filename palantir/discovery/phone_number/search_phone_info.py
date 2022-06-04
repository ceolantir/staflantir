from typing import Dict, Any

import requests

from palantir.discovery.phone_number import exceptions
from palantir.models import PhoneNumberInfo


class PhoneNumber:
    def __init__(self):
        self._base_url = 'https://htmlweb.ru/geo/api.php?json&telcod='

    def __call__(self, phone: str, specialist) -> None:
        phone_number_info = self._search_phone(phone)

        self._record_info(specialist, phone_number_info, int(phone))

    def _search_phone(self, phone: str) -> Dict[str, Any]:
        url = self._base_url + phone

        try:
            response = requests.get(url).json()

            return self._get_info_from_response(response)
        except Exception as e:
            raise exceptions.PhoneError(f'PhoneError')

    @staticmethod
    def _get_info_from_response(response: Dict[str, Any]) -> Dict[str, Any]:
        github_data_specialist = {}
        for key, value in response.items():
            if key == 'fullname':
                github_data_specialist['country'] = value
                continue
            elif key == 'okrug':
                github_data_specialist['okrug'] = value
                continue
            elif key == 'region':
                github_data_specialist[key] = value['name']
                continue
            elif key == 'tz':
                github_data_specialist['time_zone'] = value
                continue
            elif key == '0':
                github_data_specialist['oper_brand'] = value['oper_brand']
                continue

        return github_data_specialist

    @staticmethod
    def _record_info(
        specialist,
        phone_number_info: Dict[str, Any],
        phone: int,
    ) -> None:
        phone_number_specialist_info = PhoneNumberInfo.objects.update_or_create(
            specialist=specialist,
            phone=phone,
        )[0]
        for key, value in phone_number_info.items():
            setattr(phone_number_specialist_info, key, value)
        phone_number_specialist_info.save()
