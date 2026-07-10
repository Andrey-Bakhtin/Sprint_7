import requests
import allure
from urls import URL


class OrderMethods:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(body):
        return requests.post(url=URL.ORDERS, json=body)
    
    @staticmethod
    @allure.step('Получить список заказов')
    def get_order_list():
        return requests.get(url=URL.ORDERS)
    
