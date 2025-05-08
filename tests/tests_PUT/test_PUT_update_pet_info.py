import pytest
import requests
from conftest import UPDATE_PET_URL


# тест обновление информации о питомце
@pytest.mark.parametrize(
    "new_name, new_type, new_age",
    [
        ("огогошенька", "Кот767", 5)
    ]
)
def test_update_pet_info(api_key, pets_client, new_name, new_type, new_age):

    # список питомцев
    get_response = pets_client.get_all_pets()
    assert get_response.status_code == 200, "не удалось получить список питомцев"

    pets = get_response.json().get("pets", [])
    assert pets, "нет доступных питомцев для обновления"

    pet_id = pets[0]['id']  # обновить первого питомца

    update_data = {
        "name": new_name,
        "animal_type": new_type,
        "age": new_age
    }

    response = requests.put(
        f"{UPDATE_PET_URL}/{pet_id}",
        headers={'auth_key': api_key},
        data=update_data
    )

    assert response.status_code == 200, f"ожидали 200, а получили {response.status_code}"
    result = response.json()

    # проверка, что информация действительно обновилась
    assert result['name'] == new_name, "имя не обновлено"
    assert result['animal_type'] == new_type, "тип животного не обновлён"
    assert str(result['age']) == str(new_age), "возраст не обновлён"

    print(f"информация обновлена: {result['name']}, {result['animal_type']}, {result['age']}")
