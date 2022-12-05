from api import PetFriends
from settings import valid_login, valid_password, invalid_login, invalid_password, invalid_key
import os
import pytest

pf = PetFriends()


def generate_string(num):
    return "x" * num


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


def test_get_api_key_for_valid_user(email=valid_login, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем данные
    assert status == 200
    assert "key" in result


def test_get_api_key_for_invalid_user(email=invalid_login, password=invalid_password):
    """"Проверяем что запрос api ключа с невалидным логином и паролем вызывает ошибку 403 и не содержится key в результате"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем данные
    assert status == 403
    assert "key" not in result


def test_get_api_key_for_invalid_user_empty(email='', password=''):
    """"Проверяем что запрос api ключа с пустым логином и паролем вызывает ошибку 403 и не содержится key в результате"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем данные
    assert status == 403
    assert "key" not in result


def test_get_api_key_for_valid_user_with_invalid_password(email=valid_login, password=invalid_password):
    """"Проверяем что запрос api ключа с валидным логином и невалидным паролем вызывает ошибку 403 и не содержится key в результате"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем данные
    assert status == 403
    assert "key" not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с невалидным api ключом вызывает ошибку.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее подменяем ключ на невалидный и пытаемся получить список питомцев."""
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.get_list_of_pets(invalid_key, filter)
    assert status == 403


def test_add_new_pet_with_valid_data(name='Кошка', animal_type='Beatiful cat', age='1.5', pet_photo='images/dogi.jpg'):
    """Проверяем что можно добавить питомца с валидными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_data_simple(name='Кошка', animal_type='Beatiful cat', age=8):
    """Проверяем что можно добавить питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_data_simple_dict(name='Кошка', animal_type={}, age=8):
    """Проверяем что можно добавить питомца с невалидными данными"""
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400


def test_add_new_pet_with_invalid_data_simple_empty(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца с пустыми данными"""
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_set_photo(pet_photo='images/dogi.jpg'):
    """Проверяем что можно добавить фото питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_set_invalid_photo(pet_photo='images/picture.txt'):
    """Проверяем что можно добавить фото питомца с невалидными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", 3, "images/dogi.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() \
           and 0 < int(age) < 50 \
           and float(age) == int(age)


@pytest.mark.parametrize("name",
                         ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                          chinese_chars(), special_chars(), '123'],
                         ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese',
                              'specials', 'digit'])
@pytest.mark.parametrize("animal_type", ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(), special_chars(), '123'], ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['', '-1', '0', '1', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(), russian_chars().upper(), chinese_chars()], ids=['empty', 'negative', 'zero', 'min', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple(name, animal_type='двортерьер', age='4'):
    """Проверяем, что можно добавить питомца с различными данными"""

    # Добавляем питомца
    _, auth_key = pf.get_api_key(valid_login, valid_password)
    status, result = pf.add_new_pet_simple_hard(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    if name == '' or animal_type == '' or is_age_valid():
        assert pytest.status == 400
    else:
        assert pytest.status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
