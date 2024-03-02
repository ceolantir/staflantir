from typing import List, Dict, Any, Tuple

import requests

from palantir.discovery.github import constants
from palantir.discovery.github import exceptions
from palantir.models import GitHubProfileInfo, GitHubReposInfo


class GitHub:
    def __init__(self):
        self._base_url = 'https://api.github.com'

    def __call__(self, nickname: str, specialist) -> None:
        profile_info, repos_info = self._get_info(nickname)

        self._record_info(specialist, profile_info, repos_info)

    def _get_info(self, nickname: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        nickname = nickname.strip()

        profile_info = self._get_profile_info(nickname)

        repos_info = self._get_repos_info(nickname)

        repos_list = [repo['name'] for repo in repos_info]
        repos_contributors_info = self._get_contributors_info(nickname, repos_list)

        for repo_info in repos_info:
            repo_info['contributors_info'] = repos_contributors_info[repo_info['name']]

        return profile_info, repos_info

    def _get_profile_info(self, nickname: str) -> Dict[str, Any]:
        url = f'{self._base_url}/users/{nickname}'
        response = requests.get(url).json()

        if response.get('message', False):
            if 'API rate limit exceeded' in response['message']:
                raise exceptions.APIRateLimitExceeded('APIRateLimitExceeded')
        return self._get_info_from_response(
            response,
            constants.attributes_for_profile_info,
        )

    def _get_repos_info(self, nickname: str) -> List[Dict[str, Any]]:
        url = f'{self._base_url}/users/{nickname}/repos'
        response = requests.get(url).json()

        repos_info = []
        for repo in response:
            repos_info.append(
                self._get_info_from_response(
                    repo,
                    constants.attributes_for_repos_info
                )
            )

        return repos_info

    def _get_contributors_info(
        self,
        nickname: str,
        repos_list: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        repos_contributors_info = {}

        for repo in repos_list:
            url = f'{self._base_url}/repos/{nickname}/{repo}/contributors'
            response = requests.get(url).json()

            contributors_info = []
            for repo_info in response:
                contributors_info.append(
                    self._get_info_from_response(
                        repo_info,
                        constants.attributes_for_contributors_info
                    )
                )

            contributors_info = [
                f'{contribution["login"]}: {contribution["contributions"]}'
                for contribution in contributors_info
            ]
            repos_contributors_info[repo] = '; '.join(contributors_info)

        return repos_contributors_info

    @staticmethod
    def _get_info_from_response(response: Dict[str, Any], repos: str) -> Dict[str, Any]:
        github_data_specialist = {}
        for key, value in response.items():
            if key not in repos or value in (None, '', 0):
                continue
            github_data_specialist[key] = value

        return github_data_specialist

    @staticmethod
    def _record_info(
        specialist,
        profile_info: Dict[str, Any],
        repos_info: List[Dict[str, Any]]
    ) -> None:
        profile_specialist_info = GitHubProfileInfo.objects.update_or_create(specialist=specialist)[0]
        for key, value in profile_info.items():
            setattr(profile_specialist_info, key, value)
        profile_specialist_info.save()

        for repo_info in repos_info:
            repos_specialist_info = GitHubReposInfo.objects.update_or_create(
                profile=profile_specialist_info,
                name=repo_info['name'],
            )[0]
            for key, value in repo_info.items():
                setattr(repos_specialist_info, key, value)
            repos_specialist_info.save()
