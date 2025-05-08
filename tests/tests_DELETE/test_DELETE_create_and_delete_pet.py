import pytest
import requests
from conftest import BASE_URL

@pytest.mark.parametrize("name, animal_type, age", [
    ("Барсик", "Кот", "3"),
    ("Феликс", "Лиса", "2")
])
def test_create_and_delete_pet(api_key, name, animal_type, age):
    headers = {'auth_key': api_key}
    data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
    }

    # создание питомца без фото
    create_response = requests.post(f"{BASE_URL}api/create_pet_simple", headers=headers, data=data)
    assert create_response.status_code == 200, f"ожидали 200 при создании, а получили {create_response.status_code}"
    pet_id = create_response.json().get('id')
    assert pet_id, "ID нового питомца не найден в ответе"

    # удаление созданного питомца
    delete_response = requests.delete(f"{BASE_URL}api/pets/{pet_id}", headers=headers)
    assert delete_response.status_code == 200, f"ожидали 200 при удалении, а получили {delete_response.status_code}"

    # проверка удаления
    pets_response = requests.get(f"{BASE_URL}api/pets", headers=headers)
    assert pets_response.status_code == 200, f"Не удалось получить список питомцев после удаления: {pets_response.status_code}"
    all_ids = [pet['id'] for pet in pets_response.json().get('pets', [])]
    assert pet_id not in all_ids, "питомец не был удалён"

    print(f"ожидаемый результат: питомец {name} (ID: {pet_id}) успешно создан и удалён")


# удаление ВСЕХ питомцев пользователя!!!
def test_z_delete_all_pets(api_key):
    headers = {'auth_key': api_key}
    r = requests.get(f"{BASE_URL}api/pets", headers=headers)
    assert r.status_code == 200, f"не удалось получить список: {r.status_code}"
    pets = r.json().get('pets', [])

    for pet in pets:
        dr = requests.delete(f"{BASE_URL}api/pets/{pet['id']}", headers=headers)
        assert dr.status_code == 200, f"не смогли удалить {pet['id']}: {dr.status_code}"
    print(f"удалено {len(pets)} питомцев. База пуста.")





