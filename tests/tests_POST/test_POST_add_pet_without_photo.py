import pytest
import requests
import uuid
import time
from conftest import CREATE_PET_URL

# тест создание питомца + проверка ответа + время создания
@pytest.mark.parametrize(
    "name, animal_type, age",
    [
        ("ам", "куська", 2),
        ("Рекс", "собакен", 4)
    ]
)

def test_create_pet_without_photo(api_key, name, animal_type, age):
    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
    }

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 200, (
        f"ожидали статус 200, а получили {response.status_code}. "
        f"ответ сервера: {response.text}"
    )

    result = response.json()

    # проверка структуры ответа
    assert 'name' in result, "отсутствует поле 'name' в ответе"
    assert 'animal_type' in result, "отсутствует поле 'animal_type' в ответе"
    assert 'age' in result, "отсутствует поле 'age' в ответе"

    # проверка значений
    assert result['name'] == name, (
        f"ожидали имя '{name}', получили '{result['name']}'"
    )
    assert result['animal_type'] == animal_type, (
        f"ожидали тип '{animal_type}', получили '{result['animal_type']}'"
    )

    # проверка возраста с учетом возможного float
    try:
        age_value = float(result['age'])
        assert abs(age_value - age) < 0.1, (
            f"ожидали возраст ~{age}, получили {age_value}"
        )
    except ValueError:
        pytest.fail(f"возраст '{result['age']}' не может быть преобразован в число")

    print(f"питомец успешно создан: {result['name']} ({result['animal_type']}, {result['age']} лет)")

# тест с невалидным ключом авторизации
@pytest.mark.parametrize("invalid_key", ["", "invalid_key", "12345", None])
def test_create_pet_with_invalid_auth_key(invalid_key, name="Мурзик", animal_type="кот", age=2):
    headers = {'auth_key': invalid_key}
    data = {'name': name, 'animal_type': animal_type, 'age': age}

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 403, f"ожидали 403, получили {response.status_code}"
    print(f"ожидаемый результат: проверка с ключом '{invalid_key}': доступ запрещён как и ожидалось")


# тест с пустыми обязательными полями
@pytest.mark.parametrize("empty_field", ["name", "animal_type", "age"])
def test_create_pet_with_empty_required_fields(api_key, empty_field):
    headers = {'auth_key': api_key}
    data = {'name': "Тест", 'animal_type': "тест", 'age': 1}
    data[empty_field] = ""  # очищаем одно поле

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 400, f"ожидали 400, а получили {response.status_code}"
    print(f"ожидаемый результат: проверка с пустым полем '{empty_field}': сервер отклонил запрос")


# тест без заголовка авторизации
def test_create_pet_without_auth_header(name="Шарик", animal_type="собака", age=3):

    data = {'name': name, 'animal_type': animal_type, 'age': age}

    response = requests.post(CREATE_PET_URL, data=data)

    assert response.status_code == 401, f"Ожидали 401, получили {response.status_code}"
    print("ожидаемый результат: проверка без ключа авторизации: доступ запрещён")


# тест с невалидным возрастом
@pytest.mark.parametrize("age", ["-1", "999", "не число"])
def test_create_pet_with_invalid_age(api_key, age):
    headers = {'auth_key': api_key}
    data = {'name': "Тест", 'animal_type': "тест", 'age': age}

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
    print(f"ожидаемый результат: проверка с невалидным возрастом '{age}': сервер отклонил запрос")


# тест с превышением длины полей
def test_create_pet_with_too_long_fields(api_key):
    headers = {'auth_key': api_key}
    data = {
        'name': "Очень длинное имя больше ста символов " * 5,
        'animal_type': "Очень длинный тип животного " * 10,
        'age': 2
    }

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
    print("ожидаемый результат: проверка с длинными полями: сервер отклонил запрос")


#тест с некорректным методом
def test_create_pet_with_invalid_method(api_key):
    headers = {'auth_key': api_key}
    data = {'name': "Тест", 'animal_type': "тест", 'age': 1}

    response = requests.get(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 405, f"Ожидали 405, получили {response.status_code}"
    print("ожидаемый результат: проверка с GET-запросом: метод не разрешён")



# тест структуры ответа при добавлении питомца без фото
@pytest.mark.parametrize(
    "name, animal_type, age",
    [
        ("ам", "куська", 2),
        ("Рекс", "собакен", 4)
    ]
)
def test_create_pet_response_structure(api_key, name, animal_type, age):
    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
    }

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    assert response.status_code == 200, f"ожидали 200, а получили {response.status_code}"
    result = response.json()

    # Проверяем наличие обязательных полей в ответе
    required_fields = ['id', 'name', 'animal_type', 'age', 'created_at', 'user_id']
    for field in required_fields:
        assert field in result, f"отсутствует обязательное поле {field}"

    # Проверяем типы данных
    assert isinstance(result['id'], str), f"ожидали строку для id, но получили {type(result['id'])}"
    try:
        # проверка id является валидным UUID
        uuid.UUID(result['id'])
    except ValueError:
        assert False, f"id {result['id']} не является валидным UUID"

    assert isinstance(result['name'], str)
    assert isinstance(result['animal_type'], str)

    # преобразуем возраст в целое число перед проверкой
    try:
        age_value = int(result['age'])
    except ValueError:
        assert False, f"поле 'age' не может быть преобразовано в целое число: {result['age']}"

    assert isinstance(age_value, int), f"ожидали целое число для 'age', а вот получили {type(age_value)}"

    print(
        f"ожидаемый результат: питомец без фото успешно создан: {result['name']} ({result['animal_type']}, {age_value} лет)")

# тест проверка времени ответа
@pytest.mark.parametrize(
    "name, animal_type, age",
    [
        ("ам", "куська", 2)
    ]
)
def test_create_pet_without_photo(api_key, name, animal_type, age):
    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
    }

    # замер времени начала запроса
    start_time = time.time()

    response = requests.post(CREATE_PET_URL, headers=headers, data=data)

    # замер времени окончания запроса
    elapsed_time = time.time() - start_time

    # проверка времени ответа
    assert elapsed_time < 1, f"время ответа превысило 1 секунду: {elapsed_time:.2f} секунд"
    assert response.status_code == 200, f"ожидали 200, а вот получили {response.status_code}"

    result = response.json()
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert int(result['age']) == age

    print(f"ожидаемый результат: питомец без фото успешно создан: {result['name']} "
          f"({result['animal_type']}, {result['age']} лет). время ответа: {elapsed_time:.3f} сек.")

# тест с некорректным JSON в теле запроса
def test_create_pet_with_invalid_json(api_key):
    headers = {
        'auth_key': api_key,
        'Content-Type': 'application/json'
    }
    # не валидный JSON (строка вместо JSON)
    invalid_json = "{name: Тест, age:}"

    response = requests.post(CREATE_PET_URL, headers=headers, data=invalid_json)

    assert response.status_code in [400, 422, 500], \
        f"ожидали ошибку (400/422/500), а получили {response.status_code}"
    print("ожидаемый результат: сервер не принял невалидный JSON.")




