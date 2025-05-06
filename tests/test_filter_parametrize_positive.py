import pytest
import requests
from api.pf_api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()
BASE_URL = pf.base_url + "/api/pets"

@pytest.mark.parametrize("filter_value", ["", "my_pets"])
def test_filter_positive(filter_value):
    # ключ авторизации
    status, auth_key = pf.get_api_key(valid_email, valid_password)
    assert status == 200, "Ошибка авторизации"

    # запрос с фильтром
    headers = {"auth_key": auth_key["key"]}
    response = requests.get(BASE_URL, headers=headers, params={"filter": filter_value})

    # проверки
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert response.headers["Content-Type"] == "application/json"
    result = response.json()
    assert "pets" in result, "Ответ не содержит ключа 'pets'"
    assert isinstance(result["pets"], list), "Значение 'pets' должно быть списком"
