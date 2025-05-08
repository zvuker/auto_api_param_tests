import pytest
import requests
import os
from conftest import SET_PHOTO_URL

photo_path = r'C:\Users\admin\OneDrive\Рабочий стол\fsd1IcJ.jpeg'


# тест добавление фото к существующему питомцу
@pytest.mark.parametrize(
    "photo_path",
    [
        os.path.abspath("C:/Users/admin/OneDrive/Рабочий стол/2365080c740.jpg"),
    ]
)
def test_add_pet_photo(api_key, pets_client, photo_path):

    # список питомцев пользователя
    get_response = pets_client.get_all_pets()
    assert get_response.status_code == 200, "не удалось получить список питомцев"

    pets = get_response.json().get('pets', [])
    assert pets, "у пользователя нет питомцев, чтобы добавить фото"

    pet_id = pets[0]['id'] # первый id

    with open(photo_path, 'rb') as pet_photo:
        files = {'pet_photo': (os.path.basename(photo_path), pet_photo, 'image/jpeg')}
        headers = {'auth_key': api_key}
        response = requests.post(f"{SET_PHOTO_URL}/{pet_id}", headers=headers, files=files)

    assert response.status_code == 200, f"ожидали 200, а получили {response.status_code}"
    result = response.json()
    assert 'pet_photo' in result and result['pet_photo'], "фото не было добавлено"
    print(f"ожидаемый результат: фото успешно добавлено для питомца {result['name']} (ID: {pet_id})")


# тест добавление фото с некорректным id
@pytest.mark.parametrize("invalid_pet_id", ["", "не число", "99999999999999999999", "спец_символы@#$"])
def test_set_photo_with_invalid_pet_id(api_key, invalid_pet_id):
    headers = {'auth_key': api_key}

    with open(photo_path, 'rb') as photo_file:
        files = {'pet_photo': ('photo.jpg', photo_file, 'image/jpeg')}
        response = requests.post(f"{SET_PHOTO_URL}/{invalid_pet_id}", headers=headers, files=files)

    assert response.status_code in [400, 404], f"ожидаемый результат: надеялись на 400/404, получили {response.status_code}"

#  тест с невалидными типами файлов
@pytest.mark.parametrize("file_data", [
    ("text.txt", "text/plain", b"Not an image"),
    ("corrupt.jpg", "image/jpeg", b"Not a real image"),
    ("empty.file", "application/octet-stream", b"")
])
def test_set_photo_with_invalid_file_types(api_key, pets_client, file_data):
    # получить первого питомца
    get_response = pets_client.get_all_pets()
    assert get_response.status_code == 200, "не удалось получить список питомцев"
    pets = get_response.json().get('pets', [])
    assert pets, "у пользователя нет питомцев для теста"
    pet_id = pets[0]['id']

    # отправить невалидный файл
    headers = {'auth_key': api_key}
    files = {
        'pet_photo': (file_data[0], file_data[2], file_data[1])
    }
    response = requests.post(f"{SET_PHOTO_URL}/{pet_id}", headers=headers, files=files)

    assert response.status_code in (400, 415), f"ожидали 400 или 415, а получили {response.status_code}"


# тест повторная загрузка фото
@pytest.mark.parametrize(
    "photo_path",
    [
        os.path.abspath("C:/Users/admin/OneDrive/Рабочий стол/2365080c740.jpg"),
    ]
)
def test_add_pet_photo(api_key, pets_client, photo_path):
    # список питомцев пользователя
    get_response = pets_client.get_all_pets()
    assert get_response.status_code == 200, "не удалось получить список питомцев"

    pets = get_response.json().get('pets', [])
    assert pets, "у пользователя нет питомцев, чтобы добавить фото"

    pet_id = pets[0]['id']  # ID первого питомца

    # первая загрузка фото
    with open(photo_path, 'rb') as pet_photo:
        files = {'pet_photo': (os.path.basename(photo_path), pet_photo, 'image/jpeg')}
        headers = {'auth_key': api_key}
        response = requests.post(f"{SET_PHOTO_URL}/{pet_id}", headers=headers, files=files)

    assert response.status_code == 200, f"ожидали 200, а получили {response.status_code}"
    result = response.json()
    assert 'pet_photo' in result and result['pet_photo'], "Фото не было добавлено"
    print(f"фото успешно добавлено для питомца {result['name']} (ID: {pet_id})")

    # повторная загрузка фото
    with open(photo_path, 'rb') as pet_photo:
        files = {'pet_photo': (os.path.basename(photo_path), pet_photo, 'image/jpeg')}
        response_repeat = requests.post(f"{SET_PHOTO_URL}/{pet_id}", headers=headers, files=files)

    assert response_repeat.status_code == 400, (
        f"ожидали 400 при повторной загрузке фото, а получили {response_repeat.status_code}"
    )
    print(f"ожидаемый результат: повторная загрузка фото вызвала ошибку: {response_repeat.status_code}")








































