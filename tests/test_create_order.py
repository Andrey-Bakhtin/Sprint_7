import pytest
import allure

from api_methods.order_methods import OrderMethods
from helpers import generate_order_data


class TestCreateOrder:

    @allure.title("Тест создания заказа с различными валидными значениями параметра color")
    @allure.description("""Тест создаёт заказ с разными вариантами color.
    Ожидается: статус‑код 201; наличие поля track в ответе сервера.""")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
        None,
        [""]
    ])
    def test_create_order(self, color):
        with allure.step(f"Создать заказ с набором цветов: {color}"):
            body = generate_order_data(color)
        response = OrderMethods.create_order(body)
        response_data = response.json()
        assert response.status_code == 201, f"Ожидалось 201, но получено {response.status_code}"
        assert "track" in response_data, "Ответ не содержит поле 'track'"
        
