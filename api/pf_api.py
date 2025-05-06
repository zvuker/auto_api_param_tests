import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """клиент для API PetFriends."""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> tuple:
        """получение API-ключа."""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        return res.status_code, res.json() if res.ok else res.text

    def get_pets_list(self, auth_key: dict, filter: str = '') -> tuple:
        """получение списка питомцев."""
        headers = {'auth_key': auth_key['key']}
        params = {'filter': filter}

        res = requests.get(
            self.base_url + 'api/pets',
            headers=headers,
            params=params
        )
        return res.status_code, res.json() if res.ok else res.text