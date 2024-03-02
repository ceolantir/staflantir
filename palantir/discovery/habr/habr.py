from typing import Dict, List, Union, Any

import requests
from bs4 import BeautifulSoup

from palantir.discovery.habr import exceptions
from palantir.models import HabrProfileInfo, HabrReposInfo


class Habr:
    def __init__(self):
        self._base_url = 'https://habr.com/ru/users/'

    def __call__(self, username: str, specialist):
        self._base_url += username

        profile_info = self._get_profile_info()
        profile_info['name'] = username
        profile_posts = self._get_profile_posts()

        self._record_info(specialist, profile_info, profile_posts)

    def _get_profile_info(self) -> Dict[str, str]:
        url = f'{self._base_url}'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        defination_list = soup.find('div', 'tm-user-basic-info')
        try:
            summary_dl = defination_list.findAll('dl')
        except AttributeError:
            raise exceptions.HabrError('HabrError')
        summary = {}
        for dl in summary_dl:
            summary[dl.dt.text] = dl.dd.text.strip()

        profile_info = {}
        for key, item in summary.items():
            if 'рейтинг' in key.lower():
                profile_info['rating_place'] = item
            elif 'откуда' in key.lower():
                profile_info['location'] = item
            elif 'работает' in key.lower():
                profile_info['job'] = item
            elif 'рождения' in key.lower():
                profile_info['birthday'] = item
            elif 'зарегистрирован' in key.lower():
                profile_info['registered'] = item

        return profile_info

    def _get_profile_posts(self) -> List[Dict[str, Union[Union[int, str], Any]]]:
        url = f'{self._base_url}/posts/'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        posts = soup.find('div', 'tm-sub-page__main').findAll('article', 'tm-articles-list__item')

        posts_href = []
        for post in posts:
            post_url = 'https://habr.com' + post.div.h2.a['href']
            post_rating = post.find('span', 'tm-votes-meter__value').text
            posts_href.append({'url': post_url, 'rating': int(post_rating)})

        return posts_href

    @staticmethod
    def _record_info(
        specialist,
        profile_info: Dict[str, str],
        profile_posts: Dict[str, str]
    ) -> None:
        profile_specialist_info = HabrProfileInfo.objects.update_or_create(specialist=specialist)[0]
        for key, value in profile_info.items():
            setattr(profile_specialist_info, key, value)
        profile_specialist_info.save()

        for post in profile_posts:
            user_games_info = HabrReposInfo.objects.update_or_create(
                profile=profile_specialist_info,
                url=post['url'],
            )[0]
            for key, value in post.items():
                setattr(user_games_info, key, value)
            user_games_info.save()
