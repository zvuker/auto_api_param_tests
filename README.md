## Проект: автоматизированные параметризованные API-тесты сервиса https://petfriends.skillfactory.ru

основные сценарии работы: 

    создание
    обновление
    удаление
    добавление фото
    фильтрация
    обработка невалидных запросов
    защита от уязвимостей.


Основные API-эндпоинты:

    GET /api/key — получение API-ключа по email и паролю
    GET /api/pets — получение списка всех питомцев
    POST /api/create_pet_simple — добавление нового питомца без фото
    POST /api/pets — добавление нового питомца с фото
    PUT /api/pets/{pet_id} — обновление информации о питомце
    DELETE /api/pets/{pet_id} — удаление питомца
    POST /api/pets/set_photo/{pet_id} — добавление или обновление фото питомца


структура проекта:

tests/
├── tests_DELETE/
│   └── test_DELETE_create_and_delete_pet.py
├── tests_GET/
│   ├── test_GET_api_list.py
│   ├── test_GET_filter.py
│   ├── test_GET_PUT_uncorrect_method.py
│   └── test_GET_uncorrect_data.py
├── tests_POST/
│   ├── test_POST_add_pet_photo.py
│   ├── test_POST_add_pet_with_photo.py
│   ├── test_POST_add_pet_without_photo.py
│   └── test_POST_safety.py
├── tests_PUT/
    └── test_PUT_update_pet_info.py

tests_DELETE\
test_DELETE_create_and_delete_pet:

    тест удаление питомца
    test_create_and_delete_pet(api_key, name, animal_type, age)
    
    удаление всех питомцев пользователя
    test_z_delete_all_pets(api_key)

tests_GET\
test_GET_api_list:

    получение api ключа
    test_api_key_valid(api_key)
    
    получение списка питомцев
    test_get_all_pets(pets_client)


test_GET_filter:

    тест с различными значениями параметра filter 
    test_get_pets(auth_key, filter_param, expected_status_code, expected_content_type, expected_body)
    

tets_GET_PUT_uncorrect_method:

    тест метода, который не поддерживается
    def test_put_pets_method_not_allowed()
   

test_GET_uncorrect data:

    тест с некорректными учетными данными
    test_invalid_credentials(email, password, expected_status_code)
            
    тест GET /api/pets с некорректными auth_key
    test_get_pets_with_invalid_auth_key(auth_key, expected_status_code, expected_body)
    
    тесты с некорректным Content-Type
    test_get_pets_with_invalid_content_type(auth_key, content_type, expected_status_code, expected_body)


tests\tests_POST\
test_POST_add_pet_photo:

    тест добавление фото к существующему питомцу
    test_add_pet_photo(api_key, pets_client, photo_path)
    
    тест добавление фото с некорректным id
    test_set_photo_with_invalid_pet_id(api_key, invalid_pet_id)
    
    тест с невалидными типами файлов
    test_set_photo_with_invalid_file_types(api_key, pets_client, file_data)
    
    тест повторная загрузка фото
    test_add_pet_photo(api_key, pets_client, photo_path)


test_POST_add_pet_with_photo:

    тест добавлениt питомца с фото
    test_add_new_pet_with_photo(api_key, name, animal_type, age)
    
    добавление питомца с фото (некорректные данные)
    test_add_pet_with_invalid_data(api_key, name, animal_type, age, expected_status)
    
    добавление питомца без фото через endpoint для фото
    test_add_pet_without_photo(api_key)
    
    некорректный путь к фото
    test_add_pet_with_invalid_photo_path(api_key)


test_POST_add_pet_without_photo:

    тест добавления питомца без фото
    test_create_pet_without_photo(api_key, name, animal_type, age)
        
    тест с невалидным ключом авторизации
    test_create_pet_with_invalid_auth_key(invalid_key, name="Мурзик", animal_type="кот", age=2)
    
    тест с пустыми обязательными полями
    test_create_pet_with_empty_required_fields(api_key, empty_field)
    
    тест без заголовка авторизации
    test_create_pet_without_auth_header(name="Шарик", animal_type="собака", age=3)
    
    тест с невалидным возрастом
    test_create_pet_with_invalid_age(api_key, age)
    
    тест с превышением длины полей
    test_create_pet_with_too_long_fields(api_key)
    
    тест с некорректным методом
    test_create_pet_with_invalid_method(api_key)
    
    тест структуры ответа при добавлении питомца без фото
    test_create_pet_response_structure(api_key, name, animal_type, age)
    
    тест проверка времени ответа
    test_create_pet_without_photo(api_key, name, animal_type, age)

    тест с некорректным JSON в теле запроса
    def test_create_pet_with_invalid_json


test_POST_safety:

    тест защита от SQL-инъекций в полях name и animal_type
    def test_sql_injection(api_key, sql_injection)
    
    тест защита от XSS-атак в текстовых полях
    def test_xss_attempt(api_key, xss_attempt)


tests_PUT\
test_PUT_update_pet_info:

    тест обновление информации о питомце
    test_update_pet_info(api_key, pets_client, new_name, new_type, new_age)


запуск всех тестов (из директории проекта auto_api_param_tests):

    pytest -v
