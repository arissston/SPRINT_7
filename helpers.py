import requests
import random
import string

import urls

from datetime import date, timedelta


# метод генерирует строку из букв нижнего регистра, в параметре передаём длину строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def generate_random_number(max_value):
    return random.randint(1, max_value-1)


def generate_random_long_number(digits):
    return random.randint(10 ** (digits - 1), 10 ** digits - 1)


# метод создаёт данные курьера, для использования другими методами
def create_new_courier_data():
    # генерируем логин, пароль и имя курьера и собираем тело запроса
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    return payload


# метод регистрирует нового курьера и возвращает словарь с логином и паролем,
# а если регистрация не удалась, поднимает ошибку с кодом и телом ответа
def register_new_courier_and_return_login_password():
    payload = create_new_courier_data()

    response_register = requests.post(urls.COURIER_URL, data=payload)

    if response_register.status_code != 201:
        raise RuntimeError(
            f'Не удалось зарегистрировать курьера: '
            f'{response_register.status_code} {response_register.text}'
        )

    payload_for_login = {
        "login": payload["login"],
        "password": payload["password"]}

    return payload_for_login


def create_new_order_data():

    def get_tomorrow_date():
        tomorrow = date.today() + timedelta(days=1)
        return tomorrow.isoformat()

    # генерируем данные и собираем тело запроса
    payload = {
        "firstName": generate_random_string(10),
        "lastName": generate_random_string(10),
        "address": generate_random_string(10),
        "metroStation": str(generate_random_number(10)),
        "phone": str(generate_random_long_number(11)),
        "rentTime": generate_random_number(10),
        "deliveryDate": get_tomorrow_date(),
        "comment": generate_random_string(10),
    }

    return payload


def create_new_order():
    payload = create_new_order_data()
    response_create_order = requests.post(urls.ORDERS_URL, data=payload)

    if response_create_order.status_code != 201:
        raise RuntimeError(
            f'Не удалось создать заказ: '
            f'{response_create_order.status_code} {response_create_order.text}'
        )

    track_number = response_create_order.json().get("track")

    return track_number
