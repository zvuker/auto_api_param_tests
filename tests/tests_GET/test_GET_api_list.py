# тест получение API ключа
def test_api_key_valid(api_key):
    assert isinstance(api_key, str), "ключ должен быть строкой"
    assert len(api_key) > 32, "ключ слишком короткий"

# тест получения списка питомцев
def test_get_all_pets(pets_client):

    response = pets_client.get_all_pets()
    assert response.status_code == 200, f"ожидался статус 200, а получен {response.status_code}"

    data = response.json()
    assert 'pets' in data, "ответ должен содержать поле 'pets'"
    assert isinstance(data['pets'], list), "поле 'pets' должно быть списком"

    if data['pets']:
        sample_pet = data['pets'][0]
        assert 'id' in sample_pet, "у питомца должно быть поле 'id'"
        assert 'name' in sample_pet, "у питомца должно быть поле 'name'"


