import pytest
import requests
from api.pf_api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()
BASE_URL = pf.base_url + "/api/pets"

@pytest.mark.parametrize("email,password,expected_status", [
    (valid_email, valid_password, 200),  # валидный логин/пароль
    ("invalid@mail.com", valid_password, 403),  # невалидный логин
    (valid_email, "wrong_password", 403),  # невалидный пароль
])
def test_get_api_key(email, password, expected_status):
    """получение API-ключа с различными параметрами авторизации"""
    status, result = pf.get_api_key(email, password)
    assert status == expected_status, f"Ожидался статус {expected_status}, получен {status}"

    if status == 200:
        assert "key" in result, "В ответе отсутствует ключ авторизации"
        print(f"\nУспешная авторизация. Ключ: {result['key'][:5]}...")
    else:
        # проверка, является ли ответ HTML-страницей
        if isinstance(result, str) and "<html" in result.lower():
            assert "403" in result or "forbidden" in result.lower(), "Ответ не содержит ожидаемой ошибки"
            return  # завершить тест
        # если не HTML — должен быть словарь
        assert isinstance(result, dict), f"Ожидался словарь или HTML, получено: {type(result).__name__}"


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



