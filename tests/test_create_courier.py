import allure
import pytest
import requests

import urls


@allure.feature('Ручка «Создать курьера»')
class TestCreateCourier:

    @allure.title('Проверяем, что курьера можно создать и код ответа 201')
    def test_create_courier_returns_201(self, create_courier_data):

        response = requests.post(urls.COURIER_URL, data=create_courier_data)

        assert response.status_code == 201

    @allure.title('Проверяем, что успешный запрос возвращает "ok":true')
    def test_create_courier_returns_ok_true(self, create_courier_data):

        response = requests.post(urls.COURIER_URL, data=create_courier_data)

        assert response.json() == {"ok": True}

    @allure.title('Проверяем, что нельзя создать двух одинаковых курьеров и возвращается код 409')
    def test_create_courier_with_duplicate_login_returns_409(self, create_courier_data):

        requests.post(urls.COURIER_URL, data=create_courier_data)
        response = requests.post(urls.COURIER_URL, data=create_courier_data)

        assert response.status_code == 409

    @allure.title('Проверяем, что нельзя создать двух одинаковых курьеров и возвращается сообщение о дубль логине')
    def test_create_courier_with_duplicate_login_returns_mistake_message(self, create_courier_data):

        requests.post(urls.COURIER_URL, data=create_courier_data)
        response = requests.post(urls.COURIER_URL, data=create_courier_data)

        assert 'Этот логин уже используется. Попробуйте другой.' in response.json()['message']

    @allure.title('Проверяем, что если поле {field} не заполнено, запрос возвращает ошибку 400')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_without_required_field_returns_400(self, create_courier_data, field):

        payload = {k: v for k, v in create_courier_data.items() if k != field}

        response = requests.post(urls.COURIER_URL, data=payload)
        assert response.status_code == 400

    @allure.title('Проверяем, что если поле {field} не заполнено, возвращается сообщение о недостатке данных')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_without_required_field_returns_mistake_message(self, create_courier_data, field):

        payload = {k: v for k, v in create_courier_data.items() if k != field}

        response = requests.post(urls.COURIER_URL, data=payload)
        assert 'Недостаточно данных для создания учетной записи' in response.json()['message']
