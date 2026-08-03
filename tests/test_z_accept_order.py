import allure
import pytest

from api import CourierApi, OrdersApi


@allure.feature('Ручка «Принять заказ»')
class TestAcceptOrder:

    @allure.title('Проверка, что успешный запрос возвращает "ok":true')
    def test_accept_order_returns_ok_true(self, create_courier, create_order):

        login_response = CourierApi.login_courier(create_courier)
        courier_id = login_response.json().get('id')

        order_by_number_response = OrdersApi.get_order_by_track(create_order)
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = OrdersApi.accept_order(order_id, courier_id)

        assert order_response.json() == {"ok": True}

    @allure.title('Проверка, что если не передать id курьера, вернётся код 400')
    def test_accept_order_no_courier_id_return_400(self, create_order):

        order_by_number_response = OrdersApi.get_order_by_track(create_order)
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = OrdersApi.accept_order(order_id)

        assert order_response.status_code == 400

    @allure.title('Проверка, что если не передать id курьера, вернётся сообщение об ошибке')
    def test_accept_order_no_courier_id_return_mistake_message(self, create_order):

        order_by_number_response = OrdersApi.get_order_by_track(create_order)
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = OrdersApi.accept_order(order_id)

        assert 'Недостаточно данных для поиска' in order_response.json()['message']

    @allure.title('Проверка, что если передать неверный id курьера, вернётся код 404')
    def test_accept_order_wrong_courier_id_return_400(self, create_order):

        order_by_number_response = OrdersApi.get_order_by_track(create_order)
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = OrdersApi.accept_order(order_id, 987654321)

        assert order_response.status_code == 404

    @allure.title('Проверка, что если передать неверный id курьера, вернётся сообщение об ошибке')
    def test_accept_order_wrong_courier_id_return_mistake_message(self, create_order):

        order_by_number_response = OrdersApi.get_order_by_track(create_order)
        order_id = order_by_number_response.json().get("order").get("id")

        order_response = OrdersApi.accept_order(order_id, 987654321)

        assert 'Курьера с таким id не существует' in order_response.json()['message']

    @allure.title('Проверка, что если не передать id заказа, вернётся код 400')
    @pytest.mark.xfail(
        strict=True,
        reason='Баг: Принятие заказа без Id заказа возвращает код 404 вместо 400')
    def test_accept_order_no_order_id_return_400(self, create_courier):

        login_response = CourierApi.login_courier(create_courier)
        courier_id = login_response.json().get('id')

        order_response = OrdersApi.accept_order(courier_id=courier_id)

        assert order_response.status_code == 400

    @allure.title('Проверка, что если не передать id заказа, вернётся сообщение об ошибке')
    @pytest.mark.xfail(
        strict=True,
        reason='Баг: Принятие заказа без Id заказа возвращает "Not Found." вместо ожидаемого сообщения')
    def test_accept_order_no_order_id_return_mistake_message(self, create_courier):

        login_response = CourierApi.login_courier(create_courier)
        courier_id = login_response.json().get('id')

        order_response = OrdersApi.accept_order(courier_id=courier_id)

        assert 'Недостаточно данных для поиска' in order_response.json()['message']

    @allure.title('Проверка, что если передать неверный id заказа, вернётся код 404')
    def test_accept_order_wrong_order_id_return_400(self, create_courier):

        login_response = CourierApi.login_courier(create_courier)
        courier_id = login_response.json().get('id')

        order_response = OrdersApi.accept_order(987654321, courier_id)

        assert order_response.status_code == 404

    @allure.title('Проверка, что если передать неверный id заказа, вернётся сообщение об ошибке')
    def test_accept_order_wrong_order_id_return_mistake_message(self, create_courier):

        login_response = CourierApi.login_courier(create_courier)
        courier_id = login_response.json().get('id')

        order_response = OrdersApi.accept_order(987654321, courier_id)

        assert 'Заказа с таким id не существует' in order_response.json()['message']
