import requests
from conftest import GET_PETS_URL

# тест метода PUT вместо GET
def test_put_pets_method_not_allowed():
    headers = {'auth_key': "valid_api_key"}
    params = {"filter": "my_pets"}

    response = requests.put(GET_PETS_URL, headers=headers, params=params)

    # проверка кода состояния
    assert response.status_code == 405, (
        f"ожидали статус 405 (Method Not Allowed), "
        f"получили {response.status_code}"
    )

    # более гибкая проверка текста ошибки
    error_message = response.text.lower()
    assert "method not allowed" in error_message or "not allowed" in error_message, (
        f"не найдено ожидаемое сообщение об ошибке. "
        f"фактический ответ: {response.text}"
    )