import requests

import urls


class CourierApi:

    @staticmethod
    def create_courier(payload):
        return requests.post(urls.COURIER_URL, data=payload)

    @staticmethod
    def login_courier(payload, timeout=None):
        return requests.post(urls.LOGIN_COURIER_URL, data=payload, timeout=timeout)

    @staticmethod
    def delete_courier(courier_id=''):
        return requests.delete(f'{urls.COURIER_URL}/{courier_id}')


class OrdersApi:

    @staticmethod
    def create_order(payload):
        return requests.post(urls.ORDERS_URL, json=payload)

    @staticmethod
    def get_orders_list():
        return requests.get(urls.ORDERS_URL)

    @staticmethod
    def get_order_by_track(track_number=None):
        return requests.get(urls.GET_ORDER_BY_TRACK_URL, params={'t': track_number})

    @staticmethod
    def accept_order(order_id='', courier_id=None):
        return requests.put(f'{urls.ACCEPT_ORDER_URL}/{order_id}',
                            params={'courierId': courier_id})

    @staticmethod
    def cancel_order(track_number):
        return requests.put(urls.CANCEL_ORDER_URL, params={'track': track_number})
