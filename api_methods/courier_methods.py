import requests
import allure
from urls import URL


class CourierMethods:

    @staticmethod
    @allure.step('Авторизовать курьера')
    def login_courier(body):
        return requests.post(url=URL.LOGIN_COURIER, json=body)

    @staticmethod
    @allure.step('Создать курьера')
    def create_courier(body):
        return requests.post(url=URL.COURIER, json=body)
    
    @staticmethod
    @allure.step('Удалить курьера')
    def delete_courier(courier_id):
        return requests.delete(url=f"{URL.COURIER}/{courier_id}")
