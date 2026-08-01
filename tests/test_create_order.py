import allure
import pytest
import requests

import urls
import helpers


@allure.feature('Ручка «Создать заказ»')
class TestCreateOrder:

    ORDER_COLORS = [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []]

    @allure.title('Проверка, что можно указать цвет (*один, два или никакой): {color} и вернётся код 201')
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_create_order_with_color_returns_201(self, created_tracks, color):

        payload = helpers.create_new_order_data()
        payload["color"] = color

        response = requests.post(urls.ORDERS_URL, json=payload)

        track_number = response.json().get("track")
        created_tracks.append(track_number)

        assert response.status_code == 201

    @allure.title('Проверка, что можно указать цвет (*один, два или никакой): {color} и в ответе есть track')
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_create_order_with_color_contains_track(self, created_tracks, color):

        payload = helpers.create_new_order_data()
        payload["color"] = color

        response = requests.post(urls.ORDERS_URL, json=payload)

        assert "track" in response.json()

        created_tracks.append(response.json()['track'])
