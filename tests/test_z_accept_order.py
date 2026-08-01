import allure
import requests
import pytest

import urls


@allure.feature('Ручка «Принять заказ»')
class TestAcceptOrder:

    @allure.title('Проверка, что успешный запрос возвращает "ok":true')
    def test_accept_order_returns_ok_true(self, create_courier, create_order):

        login_response = requests.post(urls.LOGIN_COURIER_URL, data=create_courier)
        courier_id = login_response.json().get('id')

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': create_order})
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = requests.put(f'{urls.ACCEPT_ORDER_URL}/{order_id}', params={"courierId": courier_id})

        assert order_response.json() == {"ok": True}

    @allure.title('Проверка, что если не передать id курьера, вернётся код 400')
    def test_accept_order_no_courier_id_return_400(self, create_order):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': create_order})
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = requests.put(f'{urls.ACCEPT_ORDER_URL}/{order_id}')

        assert order_response.status_code == 400

    @allure.title('Проверка, что если передать неверный id курьера, вернётся код 404')
    def test_accept_order_wrong_courier_id_return_400(self, create_order):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': create_order})
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = requests.put(f'{urls.ACCEPT_ORDER_URL}/{order_id}', params={"courierId": 987654321})

        assert order_response.status_code == 404

    @allure.title('Проверка, что если не передать id заказа, вернётся код 400')
    @pytest.mark.xfail(
        strict=True,
        reason='Баг: Принятие заказа без Id заказа возвращает 404 "Not Found." вместо 400')
    def test_accept_order_no_order_id_return_400(self, create_courier):

        login_response = requests.post(urls.LOGIN_COURIER_URL, data=create_courier)
        courier_id = login_response.json().get('id')

        order_response = requests.put(f'{urls.ACCEPT_ORDER_URL}/', params={"courierId": courier_id})

        assert order_response.status_code == 400

    @allure.title('Проверка, что если передать неверный id заказа, вернётся код 404')
    def test_accept_order_wrong_order_id_return_400(self, create_courier):

        login_response = requests.post(urls.LOGIN_COURIER_URL, data=create_courier)
        courier_id = login_response.json().get('id')

        order_response = requests.put(f'{urls.ACCEPT_ORDER_URL}/987654321', params={"courierId": courier_id})

        assert order_response.status_code == 404
