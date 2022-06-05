from typing import Dict, Any

import requests

from palantir.discovery.stackoverflow import exceptions
from palantir.models import StackOverflowProfileInfo


class StackOverflow:
    def __init__(self):
        self._base_url = 'https://ru.stackoverflow.com'

    def __call__(self, username: str, specialist) -> None:
        profile_url = self._get_profile_url(username)
        profile_info = self._get_profile_info(profile_url)
        profile_info['name'] = username

        self._record_info(specialist, profile_info)

    def _get_profile_url(self, username: str) -> str:
        search_url = f'{self._base_url}/users?tab=Reputation&filter=all&search={username}'
        search_raw = requests.get(search_url)
        if search_raw.status_code != 200:
            raise exceptions.StackOverflowError('StackOverflowError')

        search_str = None
        for line in search_raw.text.splitlines():
            if line.find('gravatar-wrapper-48') != -1:
                search_str = line
        if not search_str:
            raise exceptions.StackOverflowError('StackOverflowError')

        return search_str.split('><')[0].split('"')[1]

    def _get_profile_info(self, profile_href: str) -> Dict[str, str]:
        profile_url = self._base_url + profile_href
        profile_raw = requests.get(profile_url)
        if profile_raw.status_code != 200:
            raise exceptions.StackOverflowError('StackOverflowError')
        profile_stats = []
        for line in profile_raw.text.splitlines():
            if line.find('fs-body3 fc-dark') != -1:
                profile_stats.append(line.split('>')[1][0])
        if not profile_stats:
            raise exceptions.StackOverflowError('StackOverflowError')

        return {
            'reputation': profile_stats[0],
            'affected': profile_stats[1],
            'answers': profile_stats[2],
            'questions': profile_stats[3],
        }

    @staticmethod
    def _record_info(
        specialist,
        profile_info: Dict[str, Any],
    ) -> None:
        profile_specialist_info = StackOverflowProfileInfo.objects.update_or_create(specialist=specialist)[0]
        for key, value in profile_info.items():
            setattr(profile_specialist_info, key, value)
        profile_specialist_info.save()
