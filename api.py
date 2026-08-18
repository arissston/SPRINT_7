import allure
import requests

import urls


class CourierApi:

    @staticmethod
    @allure.step('Создать курьера')
    def create_courier(payload):
        return requests.post(urls.COURIER_URL, data=payload)

    @staticmethod
    @allure.step('Авторизовать курьера')
    def login_courier(payload, timeout=None):
        return requests.post(urls.LOGIN_COURIER_URL, data=payload, timeout=timeout)

    @staticmethod
    @allure.step('Удалить курьера с id {courier_id}')
    def delete_courier(courier_id=''):
        return requests.delete(f'{urls.COURIER_URL}/{courier_id}')


class OrdersApi:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(payload):
        return requests.post(urls.ORDERS_URL, json=payload)

    @staticmethod
    @allure.step('Получить список заказов')
    def get_orders_list():
        return requests.get(urls.ORDERS_URL)

    @staticmethod
    @allure.step('Получить заказ по треку {track_number}')
    def get_order_by_track(track_number=None):
        return requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': track_number})

    @staticmethod
    @allure.step('Принять заказ {order_id} курьером {courier_id}')
    def accept_order(order_id='', courier_id=None):
        return requests.put(f'{urls.ACCEPT_ORDER_URL}/{order_id}',
                            params={'courierId': courier_id})

    @staticmethod
    @allure.step('Отменить заказ с треком {track_number}')
    def cancel_order(track_number):
        return requests.put(urls.CANCEL_ORDER_URL, params={'track': track_number})
