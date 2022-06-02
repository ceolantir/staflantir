import time
from typing import NamedTuple, Union, List, Any, Dict, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import requests
from networkx import Graph

from palantir.discovery.vk import constants, exceptions


class GraphVertices(NamedTuple):
    quantity: str
    average_cluster_coefficient: str
    average_degree: str


class VK:
    def __init__(self, central_user_id: str):
        self._vk_access_token = 'cd1849881f3133a4cd0f6330a699d5eb4ee611c839463512df97b0df7dc467664b9f25bf530c10d453b57'
        self._central_user_id = central_user_id

    def get_vk_info(self, visualization_friends: bool = False) -> Dict[str, Any]:
        basic_info = self._get_basic_info()
        self._check_basic_info(basic_info)

        if basic_info['is_closed'] == 'Открыт' and visualization_friends:
            number_of_friends, picture_name = self._get_graph_plot_and_number_of_friends()
            basic_info['number_of_friends'], basic_info['picture_name'] = number_of_friends, picture_name

        return basic_info

    def _get_basic_info(self) -> Dict[str, Any]:
        url = f'https://api.vk.com/method/users.get?' \
              f'access_token={self._vk_access_token}&' \
              f'user_ids={self._central_user_id}&' \
              f'fields={",".join(constants.fields)}&' \
              f'v=5.131'
        response = requests.get(url).json()
        response = response["response"]
        if not response:
            raise exceptions.BadUserID
        else:
            if response[0].get('error', False):
                self.response_processing(response)
            return response[0]

    @staticmethod
    def _check_basic_info(basic_info: Dict[str, Any]) -> None:
        for key in list(basic_info):
            if basic_info[key] in ('', 0, [], {}):
                basic_info.pop(key)
            elif key in ('city', 'country'):
                title = basic_info[key]['title']
                basic_info.pop(key)
                basic_info[key] = title
            elif key == 'occupation':
                basic_info[basic_info[key]['type']] = basic_info[key]['name']
                basic_info.pop(key)
            elif key == 'career':
                career = []
                for key_career in list(basic_info['career']):
                    if key_career.get('from', False) and key_career.get('until', False):
                        career.append(
                            f'{key_career["company"]} с {key_career["from"]} года по {key_career["until"]} год'
                        )
                    elif key_career.get('from', False):
                        career.append(
                            f'{key_career["company"]} с {key_career["from"]} года'
                        )
                    elif key_career.get('until', False):
                        career.append(
                            f'{key_career["company"]} по {key_career["until"]} год'
                        )
                basic_info['career'] = ';/n'.join(career)
            elif key == 'military':
                military = []
                for key_military in list(basic_info[key]):
                    if key_military.get('from', False) and key_military.get('until', False):
                        military.append(f'{key_military["unit"]} с {key_military["from"]} года по {key_military["until"]} год')
                    elif key_military.get('from', False):
                        military.append(f'{key_military["unit"]} с {key_military["from"]} года')
                    elif key_military.get('until', False):
                        military.append(f'{key_military["unit"]} по {key_military["until"]} год')
                basic_info['military'] = ';/n'.join(military)
            elif key == 'schools':
                schools = []
                for key_schools in list(basic_info[key]):
                    if key_schools.get('year_from', False) and key_schools.get('year_graduated', False):
                        schools.append(f'{key_schools["name"]} с {key_schools["year_from"]} года по {key_schools["year_graduated"]} год')
                    elif key_schools.get('year_from', False):
                        schools.append(f'{key_schools["name"]} с {key_schools["year_from"]} года')
                    elif key_schools.get('year_graduated', False):
                        schools.append(f'{key_schools["name"]} по {key_schools["year_graduated"]} год')
                basic_info['schools'] = ';/n'.join(schools)
            elif key == 'universities':
                universities = []
                for key_universities in list(basic_info[key]):
                    if key_universities.get('year_from', False) and key_universities.get('year_graduated', False):
                        universities.append(f'{key_universities["name"]} {key_universities["education_status"]} по {key_universities["graduation"]} год')
                    elif key_universities.get('year_from', False):
                        universities.append(f'{key_universities["name"]} {key_universities["education_status"]}')
                    elif key_universities.get('education_status', False):
                        universities.append(f'{key_universities["name"]} по {key_universities["graduation"]} год')
                basic_info['universities'] = ';/n'.join(universities)
            elif key == 'personal':
                if basic_info[key].get('political', False):
                    basic_info['political'] = constants.user_personal['political'][basic_info[key]['political']]
                elif basic_info[key].get('people_main', False):
                    basic_info['people_main'] = constants.user_personal['people_main'][basic_info[key]['people_main']]
                elif basic_info[key].get('life_main', False):
                    basic_info['life_main'] = constants.user_personal['life_main'][basic_info[key]['life_main']]
                elif basic_info[key].get('smoking', False):
                    basic_info['smoking'] = constants.user_personal['smoking'][basic_info[key]['smoking']]
                elif basic_info[key].get('alcohol', False):
                    basic_info['alcohol'] = constants.user_personal['alcohol'][basic_info[key]['alcohol']]
                elif basic_info[key].get('religion', False):
                    basic_info['religion'] = basic_info[key]['religion']
                elif basic_info[key].get('inspired_by', False):
                    basic_info['inspired_by'] = basic_info[key]['inspired_by']
                basic_info.pop(key)
            elif key == 'relation':
                basic_info[key] = constants.user_personal[key][basic_info[key]]
            elif key == 'can_access_closed':
                basic_info['is_closed'] = 'Закрыт' if not basic_info[key] else 'Открыт'
                basic_info.pop(key)
            elif key == 'is_closed':
                if basic_info[key] in ('Закрыт', 'Открыт'):
                    continue
                basic_info['is_closed'] = 'Закрыт' if basic_info[key] else 'Открыт'
            elif key in ('faculty', 'university'):
                basic_info.pop(key)
            elif key == 'id':
                basic_info['vk_id'] = basic_info[key]
                basic_info.pop(key)

    def _get_graph_plot_and_number_of_friends(self) -> Tuple[int, str]:
        graph, central_users = self._get_graph()
        picture_name = f'static/friends_graph_{self._central_user_id}.png'

        self._graph_save(graph, picture_name)

        return len(central_users), picture_name

    def _get_graph(self) -> Tuple[Graph, Dict[int, str]]:
        graph_data = {}
        central_users = self._get_central_users()

        for user_id in central_users.keys():
            graph_data[user_id] = self._get_friends(user_id)
        graph = nx.Graph()
        for user_id, user_friends in graph_data.items():
            graph.add_node(central_users[user_id])
            if not user_friends:
                continue
            for friend_id in user_friends:
                if friend_id in central_users:
                    graph.add_edge(central_users[user_id], central_users[friend_id])

        return graph, central_users

    def _get_central_users(self) -> Dict[int, str]:
        central_users = self._get_friends(with_name=True)
        central_users_dict = {
            user_dict['id']: user_dict.get('first_name') + ' ' + user_dict.get('last_name')
            for user_dict in central_users
        }
        central_users_dict[self._central_user_id] = 'Я'

        return central_users_dict

    def _get_friends(self, user_id: int = None, with_name: bool = False) -> Union[List[Any], Any]:
        if not user_id:
            user_id = self._central_user_id
        fields = 'first_name,last_name' if with_name else ''

        url = f'https://api.vk.com/method/friends.get?' \
              f'access_token={self._vk_access_token}&' \
              f'user_id={user_id}&' \
              f'fields={fields}&' \
              f'v=5.131'
        response = requests.get(url).json()
        if response.get('error'):
            if self._central_user_id == user_id:
                self.response_processing(response)
            else:
                return

        return response.get('response').get('items')

    @staticmethod
    def response_processing(response: Dict[str, Dict[str, Any]]) -> None:
        if response.get('error').get('error_msg') == 'This profile is private':
            raise exceptions.ProfileIsPrivate
        elif response.get('error').get('error_msg') == 'User was deleted or banned':
            raise exceptions.UserDeletedOrBanned
        elif response.get('error').get('error_msg') == 'Too many requests per second':
            time.sleep(1)
        else:
            raise exceptions.UnidentifiedError

    @staticmethod
    def _graph_save(graph: Graph, picture_name: str, with_labels: bool = False, **kwargs) -> None:
        plt.figure(figsize=(60, 45))
        nx.draw_kamada_kawai(graph, with_labels=with_labels, node_size=1000, width=1.5, **kwargs)
        plt.savefig(picture_name)


# if __name__ == "__main__":
#     user_id = '144816537'
#     vk_frineds_visualization = VK(user_id)
#
#     info = vk_frineds_visualization.get_vk_info()
#
#     for key, value in info.items():
#         print(key, ':', value)
