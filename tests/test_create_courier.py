import allure
import pytest

from api_methods.courier_methods import CourierMethods
from helpers import generate_courier_body

class TestCreateCourier:

    @allure.title("Тест создания нового курьера")
    @allure.description("""Тест проверяет успешное создание курьера с использованием валидных данных.
    Ожидается: статус‑код 201; значение поля ok в ответе равно True.""")
    def test_create_courier_success(self):
        body = generate_courier_body()
        response = CourierMethods.create_courier(body)
        response_data = response.json()

        assert response.status_code == 201, f"Ожидалось 201, но получено {response.status_code}"
        assert response_data.get("ok") is True, "Поле 'ok' должно быть True"

    @allure.title("Тест создания курьера с некорректными данными")
    @allure.description("""Проверяется создание курьера с пустым значением в поле {invalid_field}.
    Ожидается: статус‑код 400; сообщение: «Недостаточно данных для создания учётной записи».""")
    @pytest.mark.parametrize("invalid_field, invalid_value", [
        ("login", ""),
        ("password", ""),
    ])
    def test_create_courier_empty_field_shows_error(self, invalid_field, invalid_value):
        body = generate_courier_body()
        with allure.step(f"Подготовка данных: устанавливаем пустое значение для поля {invalid_field}"):
            body[invalid_field] = invalid_value

        with allure.step("Отправка запроса на создание курьера"):
            response = CourierMethods.create_courier(body)
            response_data = response.json()

        with allure.step("Проверка результатов"):
            assert response.status_code == 400, f"Ожидался статус 400, но получено {response.status_code}"
            expected_message = "Недостаточно данных для создания учетной записи"
            assert response_data["message"] == expected_message, f"Текст сообщения не совпадает: {response_data['message']}"

    @allure.title("Тест создания курьера с повторным логином")
    @allure.description("""Тест проверяет обработку попытки создания курьера с логином, который уже зарегистрирован.
    Ожидается: статус‑код 409; сообщение об ошибке: «Этот логин уже используется. Попробуйте другой.»""")
    def test_create_courier_duplicate_login_shows_error(self, create_and_delete_courier):
        # Используем данные из фикстуры — курьер уже создан и будет удалён после теста
        existing_login = create_and_delete_courier["login"]
        existing_password = create_and_delete_courier["password"]

        with allure.step("Попытка создать второго курьера с тем же логином"):
            second_body = {
                "firstName": "Another",
                "login": existing_login,
                "password": existing_password,
            }
            response = CourierMethods.create_courier(second_body)
            response_data = response.json()

        with allure.step("Проверка результата"):
            assert response.status_code == 409, f"Ожидался 409, но получен {response.status_code}"
            expected_message = "Этот логин уже используется. Попробуйте другой."
            assert response_data["message"] == expected_message, f"Сообщение не совпадает: {response_data['message']}"
