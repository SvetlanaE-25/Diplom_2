import requests
import allure

from url import URL


class OrderMethods:

    @staticmethod
    @allure.step("Создание заказа") 
    def create_order(ingredients: list, token=None):
        payload = {"ingredients": ingredients}
        headers = {}
        if token:
            headers["Authorization"] = token
        
        return requests.post(URL.CREATE_ORDER_ENDPOINT, json=payload, headers=headers)