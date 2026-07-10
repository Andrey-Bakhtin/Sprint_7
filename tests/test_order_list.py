import allure
from api_methods.order_methods import OrderMethods


class TestOrderList:

    @allure.title("Тест успешного получения списка заказов")
    @allure.description("Тест проверяет, что система возвращает статус‑код 200 и список заказов")
    def test_get_order_list(self):
        response = OrderMethods.get_order_list()
        json_data = response.json()
        assert response.status_code == 200, f"Ожидался код 200, но получен {response.status_code}"
        assert "orders" in json_data, "В заказе отсутствует список заказов 'orders'"
        
