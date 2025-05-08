import pytest
import requests
from conftest import BASE_URL, GET_PETS_URL, INVALID_CREDENTIALS


# тест с некорректными учетными данными (почта, пароль)
@pytest.mark.parametrize("email, password, expected_status_code", INVALID_CREDENTIALS)
def test_invalid_credentials(email, password, expected_status_code):
    response = requests.get(
        f"{BASE_URL}api/key",
        auth=(email, password),
        timeout=5
    )

    assert response.status_code == expected_status_code, f"ожидали статус {expected_status_code}, а получили {response.status_code}"
    assert "Unauthorized" in response.text, "ответ не содержит сообщение об Unauthorized"

# тест с некорректным auth_key
@pytest.mark.parametrize(
    "auth_key, expected_status_code, expected_body",
    [
        ("random_string", 401, "unauthorized"),
        ("!@#$%^&*", 401, "unauthorized"),
        ("こんにちは", 401, "unauthorized"),
        ("123", 401, "unauthorized")
    ]
)
def test_get_pets_with_invalid_auth_key(auth_key, expected_status_code, expected_body):
    headers = {'auth_key': auth_key}
    params = {"filter": ""}

    response = requests.get(GET_PETS_URL, headers=headers, params=params)

    assert response.status_code == expected_status_code, f"ожидали статус {expected_status_code}, получили {response.status_code}"
    assert expected_body in response.text, f"не найдено ожидаемое сообщение об ошибке: {expected_body}"


# тесты с некорректным Content-Type
@pytest.mark.parametrize(
    "auth_key, content_type, expected_status_code, expected_body",
    [
        # тест с корректным ключом и неправильным content-type (application/xml)
        ("valid_api_key", "application/xml", 415, "unsupported content-type"),

        # тест с корректным ключом и неправильным content-type (application/x-www-form-urlencoded)
        ("valid_api_key", "application/x-www-form-urlencoded", 415, "unsupported content-type"),

        # тест с корректным ключом и неправильным content-type (application/form-data)
        ("valid_api_key", "application/form-data", 415, "unsupported content-type"),

        # тест с корректным ключом и неправильным content-type (text/plain)
        ("valid_api_key", "text/plain", 415, "unsupported content-type")
    ]
)
def test_get_pets_with_invalid_content_type(auth_key, content_type, expected_status_code, expected_body):
    headers = {'auth_key': auth_key, 'Content-Type': content_type}
    params = {"filter": "my_pets"}

    response = requests.get(GET_PETS_URL, headers=headers, params=params)

    assert response.status_code == expected_status_code, f"ожидали статус {expected_status_code}, получили {response.status_code}"
    assert expected_body in response.text, f"не найдено ожидаемое сообщение об ошибке: {expected_body}"


