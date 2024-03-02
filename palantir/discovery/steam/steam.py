from typing import Dict, Optional

import requests
import xml.etree.ElementTree as et

from palantir.discovery.steam import exceptions
from palantir.models import SteamProfileInfo, SteamReposInfo


class Steam:
    def __init__(self):
        self._base_url = 'https://steamcommunity.com/id/'

    def __call__(self, username: str, specialist) -> None:
        self._base_url += username

        user_games = self._get_user_games()
        profile_info = {
            'name': username,
            'created_at': self._get_user_created_at(),
            'lvl': self._get_user_lvl(),
            'games_number': str(len(user_games)),
            'total_hours': self._get_total_hours(user_games),
        }

        self._record_info(specialist, profile_info, user_games)

    def _get_user_created_at(self) -> Optional[str]:
        url_1 = f'{self._base_url}/?xml=1'
        xmls = requests.get(url_1).text
        xmls = et.fromstring(xmls)
        return xmls.find('memberSince').text

    def _get_user_lvl(self) -> str:
        url = f'{self._base_url}/'
        raw = requests.get(url).text

        games_str = None
        for line in raw.splitlines():
            if line.find('persona_name persona_level') != -1:
                games_str = line
        if not games_str:
            raise exceptions.SteamError('SteamError')

        return games_str.split('</span>')[-2].split('>')[-1]

    def _get_user_games(self) -> Dict[str, str]:
        url = f'{self._base_url}/games?tab=all'
        raw = requests.get(url).text

        games_str = None
        for line in raw.splitlines():
            if line.find('var rgGames') != -1:
                games_str = line
        if not games_str:
            raise exceptions.SteamError('SteamError')

        all_games = []
        games = games_str.split('},{')
        for game in games:
            game_info = game.split(',')
            game_name, game_hours_forever = None, None
            for game_info_attr in game_info:
                if '"name"' in game_info_attr:
                    game_name = game_info_attr.split('"')[-2]
                elif '"hours_forever"' in game_info_attr:
                    game_hours_forever = game_info_attr.split('"')[-2]
            if not game_name and not game_hours_forever:
                raise exceptions.SteamError('SteamError')
            all_games.append(
                {
                    'name': game_name,
                    'hours_forever': game_hours_forever,
                }
            )

        return all_games

    @staticmethod
    def _get_total_hours(user_games: Dict[str, str]) -> float:
        total_hours = 0
        for game in user_games:
            if game['hours_forever']:
                game['hours_forever'] = float(game['hours_forever'])
            else:
                game['hours_forever'] = 0
            total_hours += game['hours_forever']
        return total_hours

    @staticmethod
    def _record_info(
        specialist,
        profile_info: Dict[str, str],
        user_games: Dict[str, str]
    ) -> None:
        profile_specialist_info = SteamProfileInfo.objects.update_or_create(specialist=specialist)[0]
        for key, value in profile_info.items():
            setattr(profile_specialist_info, key, value)
        profile_specialist_info.save()

        for game in user_games:
            user_games_info = SteamReposInfo.objects.update_or_create(
                profile=profile_specialist_info,
                name=game['name'],
            )[0]
            for key, value in game.items():
                setattr(user_games_info, key, value)
            user_games_info.save()
