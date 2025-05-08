import pytest
import requests
from conftest import CREATE_PET_URL

# тест защита от SQL-инъекций в полях name и animal_type
@pytest.mark.parametrize("sql_injection", [
    "' OR '1'='1",  # базовая SQL-инъекция
    "'; DROP TABLE pets;--",  # попытка удаления таблицы
    "1' UNION SELECT * FROM users--"  # попытка доступа к другой таблице
])
def test_sql_injection(api_key, sql_injection):

    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # проверка инъекции в поле name
    data = {
        'name': sql_injection,
        'animal_type': "безопасное_значение",
        'age': 2
    }
    response_name = requests.post(CREATE_PET_URL, headers=headers, data=data)
    assert response_name.status_code == 400, f"SQL-инъекция в поле name не была отклонена: {sql_injection}"

    # проверка инъекции в поле animal_type
    data = {
        'name': "БезопасноеИмя",
        'animal_type': sql_injection,
        'age': 2
    }
    response_type = requests.post(CREATE_PET_URL, headers=headers, data=data)
    assert response_type.status_code == 400, f"SQL-инъекция в поле animal_type не была отклонена: {sql_injection}"

    print(f"SQL-инъекция '{sql_injection}' отклонена сервером")


# тест защиты от XSS-атак в текстовых полях
@pytest.mark.parametrize("xss_attempt", [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert('XSS')",
    "<svg/onload=alert('XSS')>"
])
def test_xss_attempt(api_key, xss_attempt):
    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # проверка XSS в поле name
    data = {
        'name': xss_attempt,
        'animal_type': "безопасное_значение",
        'age': 2
    }
    response_name = requests.post(CREATE_PET_URL, headers=headers, data=data)

    # ожидаем либо:
    # 1. Код 400 (неприемлемый запрос)
    # 2. Код 200, но с экранированными символами в ответе
    if response_name.status_code == 200:
        pet_data = response_name.json()
        assert pet_data['name'] != xss_attempt, "XSS-скрипт не был экранирован в поле name"
        assert "<" not in pet_data['name'] and ">" not in pet_data['name'], "HTML-теги не были удалены"
    else:
        assert response_name.status_code == 400, f"неожиданный статус код для XSS в name: {response_name.status_code}"

    # Тестируем XSS в поле animal_type
    data = {
        'name': "БезопасноеИмя",
        'animal_type': xss_attempt,
        'age': 2
    }
    response_type = requests.post(CREATE_PET_URL, headers=headers, data=data)

    if response_type.status_code == 200:
        pet_data = response_type.json()
        assert pet_data['animal_type'] != xss_attempt, "XSS-скрипт не был экранирован в поле animal_type"
        assert "<" not in pet_data['animal_type'] and ">" not in pet_data['animal_type'], "HTML-теги не были удалены"
    else:
        assert response_type.status_code == 400, f"неожиданный статус код для XSS в animal_type: {response_type.status_code}"

    print(f"XSS-попытка '{xss_attempt}' корректно обработана сервером")