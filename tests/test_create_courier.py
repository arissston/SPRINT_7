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

    @allure.title('Проверяем, что нельзя создать двух одинаковых курьеров')
    def test_create_courier_with_duplicate_login_returns_409(self, create_courier_data):

        requests.post(urls.COURIER_URL, data=create_courier_data)
        response = requests.post(urls.COURIER_URL, data=create_courier_data)

        assert response.status_code == 409

    @allure.title('Проверяем, что если поле {field} не заполнено, запрос возвращает ошибку 400')
    @pytest.mark.parametrize('field', ['login', 'password', pytest.param('firstName', marks=pytest.mark.xfail(
            strict=True,
            reason='Баг: курьер создаётся без firstName, хотя документация помечает поле обязательным'))])
    def test_create_courier_without_required_field_returns_400(self, create_courier_data, field):

        payload = {k: v for k, v in create_courier_data.items() if k != field}

        response = requests.post(urls.COURIER_URL, data=payload)
        assert response.status_code == 400
