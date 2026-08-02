import allure
import requests

import urls


@allure.feature('Ручка «Получить заказ по его номеру»')
class TestGetOrderByNumber:

    @allure.title('Проверка, что успешный запрос возвращает код 200')
    def test_get_order_by_number_returns_200(self, create_order):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': create_order})

        assert order_by_number_response.status_code == 200

    @allure.title('Проверка, что успешный запрос возвращает объект с заказом')
    def test_get_order_by_number_returns_order(self, create_order):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': create_order})

        assert 'order' in order_by_number_response.json()

    @allure.title('Проверка, что запрос без номера заказа возвращает ошибку 400')
    def test_get_order_by_number_without_number_returns_400(self):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL)

        assert order_by_number_response.status_code == 400

    @allure.title('Проверка, что запрос без номера заказа возвращает сообщение об ошибке')
    def test_get_order_by_number_without_number_returns_mistake_message(self):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL)

        assert 'Недостаточно данных для поиска' in order_by_number_response.json()['message']

    @allure.title('Проверка, что запрос с несуществующим заказом возвращает ошибку 404')
    def test_get_order_by_number_with_wrong_number_returns_404(self):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL,
                                                params={'t': 987654321})

        assert order_by_number_response.status_code == 404

    @allure.title('Проверка, что запрос с несуществующим заказом возвращает сообщение об ошибке')
    def test_get_order_by_number_with_wrong_number_returns_mistake_message(self):

        order_by_number_response = requests.get(urls.GET_ORDER_BY_TRACK_URL,
                                                params={'t': 987654321})

        assert 'Заказ не найден' in order_by_number_response.json()['message']
