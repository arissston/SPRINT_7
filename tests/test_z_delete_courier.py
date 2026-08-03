# доп. задание - удалить курьера
import allure
import pytest

from api import CourierApi


@allure.feature('Ручка «Удалить курьера»')
class TestDeleteCourier:

    @allure.title('Проверка, что успешный запрос на удаление возвращает "ok":true')
    def test_delete_courier_success_returns_ok_true(self, create_courier):

        login_payload = create_courier
        login_response = CourierApi.login_courier(login_payload)

        courier_id = login_response.json().get('id')

        response = CourierApi.delete_courier(courier_id)

        assert response.json() == {"ok": True}

    @allure.title('Проверка, что если отправить запрос без id, вернётся ошибка 400')
    @pytest.mark.xfail(
        strict=True,
        reason='Баг: удаление без id возвращает код 404 вместо 400')
    def test_delete_courier_no_id_returns_400(self):

        response = CourierApi.delete_courier()

        assert response.status_code == 400

    @allure.title('Проверка, что если отправить запрос без id, вернётся сообщение об ошибке')
    @pytest.mark.xfail(
        strict=True,
        reason='Баг: удаление без id возвращает "Not Found." вместо ожидаемого')
    def test_delete_courier_no_id_returns_mistake_message(self):

        response = CourierApi.delete_courier()

        assert 'Недостаточно данных для удаления курьера' in response.json()['message']

    @allure.title('Проверка, что если отправить запрос с несуществующим id, вернётся ошибка 404')
    def test_delete_courier_wrong_id_returns_404(self):

        response = CourierApi.delete_courier(987654321)

        assert response.status_code == 404

    @allure.title('Проверка, что если отправить запрос с несуществующим id, вернётся сообщение об ошибке')
    def test_delete_courier_wrong_id_returns_mistake_message(self):

        response = CourierApi.delete_courier(987654321)

        assert 'Курьера с таким id нет' in response.json()['message']
