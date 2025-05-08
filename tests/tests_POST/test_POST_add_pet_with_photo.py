import pytest
import os
import requests
from conftest import CREATE_PET_WITH_PHOTO_URL, SET_PHOTO_URL

PHOTO_PATH = r'C:\Users\admin\OneDrive\Рабочий стол\fsd1IcJ.jpeg'
INVALID_PHOTO_PATH = r'C:\Users\admin\OneDrive\Рабочий стол\no_such_file.jpeg'


# тест добавлениt питомца с фото
@pytest.mark.parametrize(
    "name, animal_type, age",
    [
        ("Бука_1", "годзилка4", 3),
        ("Бука_2", "годзилка5", 5),
        ("Бука_3", "годзилка6", 2)
    ]
)

def test_add_new_pet_with_photo(api_key, name, animal_type, age):
    headers = {'auth_key': api_key}

    with open(PHOTO_PATH, 'rb') as photo_file:
        files = {
            'name': (None, name),
            'animal_type': (None, animal_type),
            'age': (None, str(age)),
            'pet_photo': ('fsd1IcJ.jpeg', photo_file, 'image/jpeg')
        }

        response = requests.post(CREATE_PET_WITH_PHOTO_URL, headers=headers, files=files)

    assert response.status_code == 200, f"ожидали статус 200, а получили {response.status_code}"
    data = response.json()
    assert data['name'] == name
    assert data['animal_type'] == animal_type
    assert int(data['age']) == age
    print(f"ожидаемый результат: успешно добавлен питомец: {data['name']} ({data['animal_type']}, {data['age']} лет)")



# негативные тесты - добавление питомца с фото (некорректные данные)
@pytest.mark.parametrize(
    "name, animal_type, age, expected_status",
    [
        ("", "кошка", 2, 400),  # пустое имя
        ("Барсик", "", 3, 400),  # пустой тип животного
        ("Барсик", "кот", "", 400),  # пустой возраст
        ("Барсик", "кот", -1, 400),  # отрицательный возраст
        ("Барсик", "кот", "три", 400),  # возраст не число
    ]
)

def test_add_pet_with_invalid_data(api_key, name, animal_type, age, expected_status):

    headers = {'auth_key': api_key}

    with open(PHOTO_PATH, 'rb') as photo_file:
        files = {
            'name': (None, name),
            'animal_type': (None, animal_type),
            'age': (None, str(age)),
            'pet_photo': ('fsd1IcJ.jpeg', photo_file, 'image/jpeg')
        }

        response = requests.post(SET_PHOTO_URL, headers=headers, files=files)

    assert response.status_code == expected_status, f"ожидали статус {expected_status}, а получили {response.status_code}"
    print(f"ожидаемый результат: не удалось добавить питомца с данными: name='{name}', type='{animal_type}', age='{age}'")


# добавление питомца без фото через endpoint для фото
def test_add_pet_without_photo(api_key):
    headers = {'auth_key': api_key}

    files = {
        'name': (None, 'БезФото'),
        'animal_type': (None, 'кот'),
        'age': (None, '3'),
    }

    response = requests.post(SET_PHOTO_URL, headers=headers, files=files)

    assert response.status_code != 200, f"ожидали ошибку, а получили статус 200"
    print("ожидаемый результат: не удалось добавить питомца без фото через этот endpoint")


# некорректный путь к фото
def test_add_pet_with_invalid_photo_path(api_key):
    headers = {'auth_key': api_key}

    # проверка, что файл не существует
    assert not os.path.exists(INVALID_PHOTO_PATH), "файл по указанному пути существует — нужно указать некорректный путь"

    try:
        with open(INVALID_PHOTO_PATH, 'rb') as photo_file:
            files = {
                'name': (None, 'ОшибкаФайл'),
                'animal_type': (None, 'кот'),
                'age': (None, '3'),
                'pet_photo': ('no_such_file.jpeg', photo_file, 'image/jpeg')
            }

            response = requests.post(SET_PHOTO_URL, headers=headers, files=files)
            pytest.fail("ожидалось исключение FileNotFoundError, но запрос был выполнен")

    except FileNotFoundError:
        print("ожидаемый результат: файл не найден, исключение FileNotFoundError")
