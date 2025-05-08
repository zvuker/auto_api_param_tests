import pytest
import requests
from requests.exceptions import RequestException


BASE_URL = 'https://petfriends.skillfactory.ru/'
VALID_CREDS = {
    'email': '76@mail.com',
    'password': '2025'
}

UPDATE_PET_URL = f"{BASE_URL}api/pets"
CREATE_PET_URL = f"{BASE_URL}api/create_pet_simple"
SET_PHOTO_URL = f"{BASE_URL}api/pets/set_photo"
GET_PETS_URL = f"{BASE_URL}api/pets"
CREATE_PET_WITH_PHOTO_URL = f"{BASE_URL}api/pets"

INVALID_CREDENTIALS = [
    ("invalid_email@mail.com", "validpassword123", 401),  # невалидная почта
    ("valid_email@mail.com", "invalidpassword", 401),  # невалидный пароль
    ("invalid_email@mail.com", "invalidpassword", 401),  # невалидная почта и пароль
    ("", "validpassword123", 401),  # пустая почта
    ("valid_email@mail.com", "", 401),  # пустой пароль
    ("", "", 401),  # пустая почта и пустой пароль
]

# фикстура для получения API ключа (выполняется 1 раз на сессию тестов)
@pytest.fixture(scope='session')
def api_key():
    try:
        response = requests.get(
            f"{BASE_URL}api/key",
            headers=VALID_CREDS,  # передать email и password в headers
            timeout=5
        )
        response.raise_for_status()
        key = response.json().get('key')
        assert key, "Ключ не найден в ответе"
        return key
    except RequestException as e:
        pytest.fail(f"Ошибка при получении API ключа: {str(e)}")

# клиент для работы с API
@pytest.fixture
def pets_client(api_key):

    class PetsClient:
        def __init__(self, auth_key):
            self.headers = {'auth_key': auth_key}
            self.base_url = f"{BASE_URL}api/pets"

        def get_all_pets(self):
            return requests.get(self.base_url, headers=self.headers)

    return PetsClient(api_key)

