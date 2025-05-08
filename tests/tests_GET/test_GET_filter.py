import pytest
import requests
from requests.exceptions import RequestException
from conftest import GET_PETS_URL


@pytest.mark.parametrize(
    "auth_key, filter_param, expected_status_code, expected_content_type, expected_body",
    [
        # позитивный тест с корректным ключом и пустым фильтром
        ("valid_api_key", "", 200, "application/json", "pets"),
        # позитивный тест с фильтром "my_pets"
        ("valid_api_key", "my_pets", 200, "application/json", "pets"),
        # тест с фильтром больше 1000 символов (ожидаем ошибку 500)
        ("valid_api_key", "a" * 1001, 500, "text/html", "server error"),
        # тест с фильтром из спецсимволов (ожидаем ошибку 500)
        ("valid_api_key", "!@#$%^&*", 500, "text/html", "server error"),
        # тест с некорректным токеном (ожидаем ошибку 401)
        ("invalid_api_key", "", 401, "text/html", "unauthorized"),
        # тест с истекшим токеном (ожидаем ошибку 401)
        ("expired_api_key", "", 401, "text/html", "unauthorized"),
        # тест с фильтром как число (ожидаем ошибку 500)
        ("valid_api_key", "123", 500, "text/html", "server error"),
        # тест с фильтром иероглифы (ожидаем ошибку 500)
        ("valid_api_key", "こんにちは", 500, "text/html", "server error")
    ]
)
def test_get_pets(auth_key, filter_param, expected_status_code, expected_content_type, expected_body):
    params = {"filter": filter_param}
    headers = {'auth_key': auth_key}

    try:
        response = requests.get(GET_PETS_URL, headers=headers, params=params)

        assert response.status_code == expected_status_code, (
            f"ожидали статус {expected_status_code}, а получили {response.status_code}"
        )

        assert response.headers["Content-Type"].startswith(
            expected_content_type
        ), (
            f"ожидали content-type {expected_content_type}, "
            f"получили {response.headers['Content-Type']}"
        )

        if expected_status_code == 200:
            response_json = response.json()
            assert expected_body in response_json, (
                f"не найдено ожидаемое тело ответа: {expected_body}"
            )
        else:
            assert expected_body.lower() in response.text.lower(), (
                f"не найдено ожидаемое сообщение об ошибке: {expected_body}\n"
                f"фактический ответ: {response.text}"
            )

    except RequestException as e:
        pytest.fail(f"ошибка при выполнении запроса: {str(e)}")