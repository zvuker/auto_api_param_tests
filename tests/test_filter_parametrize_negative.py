import pytest
from api.pf_api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.mark.parametrize("invalid_filter", [
    "",  # пустая строка
    "my_pets",  # фильтр "мои питомцы"
    "a" * 255,  # строка из 255 символов
    "a" * 1001,  # строка длиной > 1000 символов
    "кириллица",  # кириллические символы
    "汉字漢字",  # китайские символы
    "!@#$%^&*()_+=<>?",  # спецсимволы
    12345  # число
])
def test_get_all_pets_with_invalid_filters(invalid_filter):
    """получение списка питомцев с некорректными значениями параметра filter (ошибка клиента)."""
    # получение ключа
    status, auth_key = pf.get_api_key(valid_email, valid_password)
    assert status == 200, "Ошибка авторизации"

    # преобразуем числовой фильтр в строку
    invalid_filter_str = str(invalid_filter)

    # список питомцев с некорректным фильтром
    status, result = pf.get_pets_list(auth_key, filter=invalid_filter_str)

    # проверяем, что сервер возвращает ошибку (4xx)
    assert status in [400, 422], f"Ожидался статус 4xx, получен {status}"
    assert isinstance(result, dict), "Ответ не является JSON-объектом"
    assert 'error' in result or 'message' in result, "Ответ не содержит ошибки"

    print(f"\nНекорректный фильтр: {repr(invalid_filter)} → Статус: {status}")
