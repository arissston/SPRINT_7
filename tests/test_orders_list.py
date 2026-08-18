import allure

from api import OrdersApi


@allure.feature('Ручка «Список заказов»')
class TestOrdersList:

    @allure.title('При получении списка заказов - должен вернуться код ответа 200')
    def test_get_orders_list_returns_200(self, create_order):

        response = OrdersApi.get_orders_list()

        assert response.status_code == 200

    @allure.title('При получении списка заказов - в тело ответа должен вернуться список заказов')
    def test_get_orders_list_returns_orders_list(self, create_order):

        response = OrdersApi.get_orders_list()

        assert 'orders' in response.json()
