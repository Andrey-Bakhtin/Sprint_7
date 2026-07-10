import pytest
import logging

from api_methods.courier_methods import CourierMethods
from helpers import generate_courier_body

logger = logging.getLogger(__name__)

@pytest.fixture
def create_and_delete_courier():
    # Создание курьера
    body = generate_courier_body()
    response = CourierMethods.create_courier(body)
    if response.status_code != 201:
        logger.warning("Курьер не был создан, статус: %s", response.status_code)

    # Авторизация для получения ID
    login_data = {
        "login": body["login"],
        "password": body["password"]
    }
    login_response = CourierMethods.login_courier(login_data)
    courier_id = login_response.json()["id"]

    # Возвращаем данные курьера и его ID
    yield {
        "login": body["login"],
        "password": body["password"],
        "id": courier_id
    }

    # Удаление курьера после теста
    delete_response = CourierMethods.delete_courier(courier_id)
    if delete_response.status_code != 200:
        logger.warning(
            "Не удалось удалить курьера с ID %s. Статус: %s, Ответ: %s",
            courier_id,
            delete_response.status_code,
            delete_response.json()
        )
