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


# метод отправляет запрос на регистрацию курьера
# и возвращает ответ сервера вместе с отправленными данными
def register_new_courier():
    payload = create_new_courier_data()
    response = requests.post(urls.COURIER_URL, data=payload)

    return response, payload


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
    response = requests.post(urls.ORDERS_URL, data=payload)

    return response
