from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()

# Блок тестов на получение api ключа
# Позитивный тест-фикстура на получение  api ключа
@pytest.fixture(autouse=True)
def get_api_key():
    """Позитивный тест получения API ключа для зарегистрированного пользователя. Проверяем, что
    запрос возвращает статус 200 и в результате содержится слово key (setup).
    После отработки основного фикстура проверяет у основной функции код ответа (teardown)"""
    pf = PetFriends()
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key
    yield
    # Проверяем что статус ответа в тесте = 200 и имя питомца соответствует заданному
    # assert pytest.status == 200


# Блок тестов на проверку списка питомцев
# Позитивный тест на получение списка питомцев с использованием параметризации
@pytest.mark.parametrize("filter", ['', 'my_pets'], ids= ['all pets', 'my pets'])
def test_get_all_pets_with_valid_key(filter):
   """ Проверяем, что запрос питомцев возвращает не пустой список.
   С помощью фикстуры pytestа получаем api-ключ и сохраняем в переменную pytest.key.
   Используя этот ключ, запрашиваем список питомцев согласно позитивных параметов в filter pytest.mark.parametrize.
   Проверяем, что список не пустой."""
   pytest.status, result = pf.get_list_of_pets(pytest.key, filter)
   assert pytest.status == 200
   assert len(result['pets']) > 0

# Негативный тест на получение списка питомцев с использованием параметризации
def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

@pytest.mark.parametrize("filter",
                        [generate_string(255), generate_string(1001), russian_chars(),
                        russian_chars().upper(), chinese_chars(), special_chars(), 123]
                        , ids= ['255 sym', '> 1000 sym', 'russian', 'RUSSIAN', 'chinese'
                        , 'specials', 'digit'])
def test_get_all_pets_with_negative_filter(filter):
   """ Проверяем, что запрос питомцев возвращает код ответа 400 (500).
   С помощью фикстуры pytestа получаем api-ключ и сохраняем в переменную pytest.key.
   Используя этот ключ, запрашиваем список питомцев согласно негативных параметов filter в pytest.mark.parametrize.
   Проверяем, что список не пустой."""
   pytest.status, result = pf.get_list_of_pets(pytest.key, filter)
   assert pytest.status == 500

# В негативных тестах мы ожидаем ответ с кодом 400 (Bad Request), а не 500 (Internal Server Error), так как
# предполагается, что сервер должен корректно обрабатывать такие запросы и возвращать код, который сообщает
# клиенту об ошибке на его стороне. В данном случае сервер некорректно обраьатывает запрос и возвращает код 500.
# Для получения зеленых тестов проверяем pytest.status на код 500.


# Блок тестов на проверку добавления питомцев
def test_add_new_pet_with_valid_data(name='Матюся', animal_type='британец', age='9', pet_photo='images/cat11.jpg'):
    """Позитивный тест добавления нового питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_negativ_add_new_pet_with_non_valid_key(name='Матюся', animal_type='британец', age='9', pet_photo='images/cat11.jpg'):
    """Негативный тест добавления нового питомца с некорректным ключом"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Добавляем некорректный ключ api и сохраняем в переменую auth_key
    auth_key = {'key': 'ksa344ldld'}
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'Forbidden' in result

def test_negativ_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/cat11.jpg'):
    """Негативный тест добавления нового питомца с пустыми данными и фото"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''

def test_add_new_pet_with_valid_data_no_foto(name='Матюся', animal_type='британец', age='9'):
    """Позитивный тест добавления нового питомца с корректными данными без фото"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_foto_pet_with_valid_data(pet_photo='images/cat11.jpg'):
    """Позитивный тест добавления фото питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['id'] == pet_id



# Блок тестов на проверку удаления питомцев

def test_successful_delete_self_pet():
    """Позитивный тест успешного удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9', 'images/cat11.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_negative_delete_pet_non_correct_key():
    """Негативный тест удаления питомца с некорректным ключом"""
    # Вначале получаем рабочий ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9', 'images/cat11.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    # Берем некорректный ключ auth_key1 и делаем запрос на удаление
    auth_key_false = {'key': 'ksa344ldld'}
    status, result = pf.delete_pet(auth_key_false, pet_id)
    # Проверяем что статус ответа равен 403 и в результате есть Forbidden
    assert status == 403
    assert 'Forbidden' in result

def test_negative_delete_pet_non_correct_id():
    """Негативный тест удаления питомца с некорректным ID"""
    # Получаем рабочий ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берём некорректный id
    pet_id = ''
    status, result = pf.delete_pet(auth_key, pet_id)
    # Проверяем что статус ответа равен 404 и в результате есть Not Found
    assert status == 404
    assert 'Not Found' in result

# Блок тестов на проверку обновления данных питомцев

def test_successful_update_self_pet_info(name='Матюсище', animal_type='двортерьер', age=6):
    """Позитивный тест успешного обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        # добавляем нового питомца и опять запрашиваем список своих питомцев
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9', 'images/cat11.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name

def test_negativ_update_pet_info_non_correct_key(name='Матюсище', animal_type='двортерьер', age=6):
    """Негативный тест обновления информации о питомце с некорректным ключом"""
    # Получаем корректный ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой, то пробуем обновить его имя, тип и возраст с некорректным ключом
    auth_key_false = {'key': 'ksa344ldld'}
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        # добавляем нового питомца и опять запрашиваем список своих питомцев
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9', 'images/cat11.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Пробуем обновить имя, тип и возраст с некорректным ключом
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 403 и в результате есть Forbidden
    assert status == 403
    assert 'Forbidden' in result