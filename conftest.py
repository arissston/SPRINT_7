# conftest.py
import pytest

import helpers
from api import CourierApi, OrdersApi


@pytest.fixture
def create_courier():
    payload = helpers.create_new_courier_data()
    CourierApi.create_courier(payload)

    login_payload = {
        'login': payload['login'],
        'password': payload['password']
    }

    # id узнаём сразу, чтобы teardown не зависел от повторного логина
    courier_id = CourierApi.login_courier(login_payload).json().get('id')

    yield login_payload

    # если тест удалил курьера сам, сервер ответит 404 — это нормально
    CourierApi.delete_courier(courier_id)


@pytest.fixture
def create_courier_data():
    payload = helpers.create_new_courier_data()

    yield payload

    # курьер мог быть создан тестом, а мог и не быть,
    # поэтому сначала пробуем залогиниться и удаляем только при успехе
    login_payload = {
        'login': payload['login'],
        'password': payload['password']
    }

    login_response = CourierApi.login_courier(login_payload)

    if login_response.status_code == 200:
        CourierApi.delete_courier(login_response.json()['id'])


@pytest.fixture
def create_order():
    payload = helpers.create_new_order_data()
    track_number = OrdersApi.create_order(payload).json().get('track')

    yield track_number

    OrdersApi.cancel_order(track_number)


@pytest.fixture
def created_tracks():
    tracks = []

    yield tracks

    for track in tracks:
        OrdersApi.cancel_order(track)
