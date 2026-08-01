import pytest
import requests

import urls
import helpers


@pytest.fixture
def create_courier():
    payload = helpers.register_new_courier_and_return_login_password()

    yield payload

    # В teardown пытаемся залогиниться этими данными и удалить курьера, если он существует:
    login_response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

    if login_response.status_code == 200:
        courier_id = login_response.json().get('id')
        requests.delete(f'{urls.COURIER_URL}/{courier_id}')


@pytest.fixture
def create_courier_data():
    payload = helpers.create_new_courier_data()

    yield payload

    # В teardown пытаемся залогиниться этими данными и удалить курьера, если он существует:
    login_payload = {
        'login': payload['login'],
        'password': payload['password']
    }

    login_response = requests.post(urls.LOGIN_COURIER_URL, data=login_payload)

    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        requests.delete(f'{urls.COURIER_URL}/{courier_id}')


@pytest.fixture
def create_order():
    track_number = helpers.create_new_order()

    yield track_number

    # В teardown удаляем созданные данные:
    requests.put(urls.CANCEL_ORDER_URL, params={'track': track_number})


@pytest.fixture
def created_tracks():
    tracks = []
    yield tracks

    for track in tracks:
        requests.put(urls.CANCEL_ORDER_URL, params={'track': track})
