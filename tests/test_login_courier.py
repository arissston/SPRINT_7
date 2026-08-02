import allure
import pytest
import requests

import urls
import helpers


@allure.feature('Ручка «Логин курьера»')
class TestLoginCourier:

    @allure.title('Проверка, что курьер может авторизоваться и код ответа 200')
    def test_login_courier_returns_200(self, create_courier):

        response = requests.post(urls.LOGIN_COURIER_URL, data=create_courier)

        assert response.status_code == 200

    @allure.title('Проверка, что успешный логин возвращает id')
    def test_login_courier_returns_id(self, create_courier):

        response = requests.post(urls.LOGIN_COURIER_URL, data=create_courier)

        assert 'id' in response.json()

    @allure.title('Проверка, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_courier_non_existent_user_returns_404(self):

        payload = {
            'login': helpers.generate_random_string(10),
            'password': helpers.generate_random_string(10)}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404

    @allure.title('Проверка - если авторизоваться под несуществующим пользователем, возвращается сообщение об ошибке')
    def test_login_courier_non_existent_user_returns_mistake_message(self):

        payload = {
            'login': helpers.generate_random_string(10),
            'password': helpers.generate_random_string(10)}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert 'Учетная запись не найдена' in response.json()['message']

    @allure.title('Проверка, что если неправильно указать логин, вернётся код 400')
    def test_login_courier_wrong_login_returns_404(self, create_courier):

        payload = {
            'login': helpers.generate_random_string(10),
            'password': create_courier['password']}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404

    @allure.title('Проверка, что если неправильно указать логин, вернётся сообщение об ошибке')
    def test_login_courier_wrong_login_returns_404_mistake_message(self, create_courier):

        payload = {
            'login': helpers.generate_random_string(10),
            'password': create_courier['password']}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert 'Учетная запись не найдена' in response.json()['message']

    @allure.title('Проверка, что если неправильно указать пароль, вернётся код 404 ')
    def test_login_courier_wrong_password_returns_404(self, create_courier):

        payload = {
            'login': create_courier['login'],
            'password': helpers.generate_random_string(10)}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404

    @allure.title('Проверка, что если неправильно указать пароль, вернётся код 404 ')
    def test_login_courier_wrong_password_returns_mistake_message(self, create_courier):

        payload = {
            'login': create_courier['login'],
            'password': helpers.generate_random_string(10)}
        response = requests.post(urls.LOGIN_COURIER_URL, data=payload)

        assert 'Учетная запись не найдена' in response.json()['message']

    @allure.title('Проверка, что если нет поля {field}, запрос возвращает ошибку')
    @pytest.mark.parametrize('field', ['login', pytest.param('password', marks=pytest.mark.xfail(
            strict=True,
            reason='Баг: логин без поля password висит 60 с и возвращает 504 вместо 400'))])
    def test_login_courier_without_required_field_returns_400(self, create_courier, field):

        payload = {k: v for k, v in create_courier.items() if k != field}

        response = requests.post(urls.LOGIN_COURIER_URL, data=payload, timeout=10)
        assert response.status_code == 400

    @allure.title('Проверка, что если нет поля {field}, запрос возвращает сообщение об ошибке')
    @pytest.mark.parametrize('field', ['login', pytest.param('password', marks=pytest.mark.xfail(
            strict=True,
            reason='Баг: логин без поля password висит 60 с и возвращает 504 вместо 400'))])
    def test_login_courier_without_required_field_returns_mistake_message(self, create_courier, field):

        payload = {k: v for k, v in create_courier.items() if k != field}

        response = requests.post(urls.LOGIN_COURIER_URL, data=payload, timeout=10)
        assert 'Недостаточно данных для входа' in response.json()['message']
