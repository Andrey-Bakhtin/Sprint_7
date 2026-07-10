import pytest
import allure

from api_methods.courier_methods import CourierMethods
from helpers import generate_random_login_password

class TestLoginCourier:

    @allure.title("Тест успешной авторизации курьера")
    @allure.description("""Тест проверяет успешную авторизацию курьера с валидными учётными данными.
    Ожидается: статус‑код 200; наличие поля id в теле ответа.""")
    def test_login_courier_existing_user_success(self, create_and_delete_courier):
        login_data = {
            "login": create_and_delete_courier["login"],
            "password": create_and_delete_courier["password"],
        }

        with allure.step("Отправка запроса на авторизацию курьера"):
            response = CourierMethods.login_courier(login_data)
            response_data = response.json()

        with allure.step("Проверка результатов авторизации"):
            assert response.status_code == 200, f"Ожидалось 200, но получено {response.status_code}"
            assert "id" in response_data, "Ответ не содержит поле 'id'"

    @allure.title("Тест авторизации с неправильным значением для поля {key}")
    @allure.description("""Тест проверяет обработку авторизации при передаче неправильного значения в поле {key}. 
    Ожидается: статус‑код 404; сообщение: «Учётная запись не найдена».""")
    @pytest.mark.parametrize("key, value", [
        ("login", "test"),
        ("password", "test")
    ])
    def test_login_courier_with_incorrect_field_shows_error(self, key, value, create_and_delete_courier):
        # Берём валидные данные из фикстуры
        body = {
            "login": create_and_delete_courier["login"],
            "password": create_and_delete_courier["password"],
        }
        # Меняем нужное поле напрямую
        body[key] = value

        with allure.step("Отправка запроса на авторизацию курьера"):
            response = CourierMethods.login_courier(body)
            data = response.json()

        with allure.step("Проверка результатов авторизации"):
            assert response.status_code == 404, f"Ожидалось 404, но получено {response.status_code}"
            expected_message = "Учетная запись не найдена"
            assert data["message"] == expected_message, f"Текст сообщения отсутствует или не совпадает: {data['message']}"

    @allure.title("Тест авторизации с пустым значением для поля {key}")
    @allure.description("""Тест проверяет обработку авторизации при передаче пустого значения в поле {key}. 
    Ожидается: статус‑код 400; сообщение об ошибке: «Недостаточно данных для входа».""")
    @pytest.mark.parametrize("key, value", [
        ("login", ""),
        ("password", "")
    ])
    def test_login_courier_with_empty_field_shows_error(self, key, value):
        # Используем случайные данные
        body = generate_random_login_password()
        # Подменяем нужное поле на пустое
        body[key] = value

        with allure.step(f"Попытка авторизации с пустым значением для поля {key}"):
            response = CourierMethods.login_courier(body)
            data = response.json()

        with allure.step("Проверка результатов авторизации"):
            assert response.status_code == 400, f"Ожидалось 400, но получено {response.status_code}"
            expected_message = "Недостаточно данных для входа"
            assert data["message"] == expected_message, f"Текст сообщения отсутствует или не совпадает: {data['message']}"

    @allure.title("Тест авторизации несуществующего пользователя")
    @allure.description("""Тест проверяет ответ системы при попытке авторизации с несуществующими учётными данными. 
    Ожидается: статус‑код 404; сообщение: «Учётная запись не найдена».""")
    def test_login_courier_with_nonexistent_user_shows_error(self):
        body = generate_random_login_password()

        with allure.step("Попытка авторизоваться со случайными учётными данными"):
            response = CourierMethods.login_courier(body)
            data = response.json()

        with allure.step("Проверка результатов авторизации"):
            assert response.status_code == 404, f"Ожидалось 404, но получено {response.status_code}"
            expected_message = "Учетная запись не найдена"
            assert data["message"] == expected_message, f"Текст сообщения отсутствует или не совпадает: {data['message']}"
