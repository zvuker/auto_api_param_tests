import pytest
from api.pf_api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


@pytest.mark.parametrize("email,password,expected_status", [
    (valid_email, valid_password, 200),  # позитивный тест
    ("invalid@mail.com", valid_password, 403),  # негативный тест
    (valid_email, "wrong_password", 403)  # негативный тест
])
def test_get_api_key(email, password, expected_status):
    """получение API-ключа с разными параметрами авторизации"""
    status, result = pf.get_api_key(email, password)

    assert status == expected_status, f"Ожидался статус {expected_status}, получен {status}"
    if status == 200:
        assert "key" in result, "В ответе отсутствует API-ключ"
        print(f"\nУспешная авторизация. Ключ: {result['key'][:5]}...")
    else:
        # Проверяем HTML-ответ на наличие текста ошибки
        error_message = "This user wasn't found in database"
        assert error_message in str(result), f"Не найдено сообщение '{error_message}'"


@pytest.mark.parametrize("filter_value", ["", "my_pets"])
def test_get_all_pets(filter_value):
    """получение списка питомцев с разными фильтрами"""
    # ключ авторизации
    status, auth_key = pf.get_api_key(valid_email, valid_password)
    assert status == 200, "Ошибка авторизации"

    # список питомцев
    status, result = pf.get_pets_list(auth_key, filter_value)

    assert status == 200, f"Ожидался статус 200, получен {status}"
    assert "pets" in result, "Ответ не содержит ключа 'pets'"
    assert isinstance(result["pets"], list), "'pets' должен быть списком"

    if filter_value == "my_pets":
        print(f"\nПолучено моих питомцев: {len(result['pets'])}")
    else:
        print(f"\nПолучено всех питомцев: {len(result['pets'])}")