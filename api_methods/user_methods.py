import requests
import allure

from url import URL


class UserMethods:

    @staticmethod
    @allure.step("Создание пользователя")
    def user_create(email, password, name):
        payload = {
        "email": email,
        "password": password,
        "name": name
    }
        return requests.post(URL.USER_REGISTRATION_ENDPOINT, data=payload)
    

    @staticmethod
    @allure.step("Авторизация пользователя в системе") 
    def user_login(email, password):
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(URL.USER_LOGIN_ENDPOINT, data=payload)
    
    @staticmethod
    @allure.step("Удаление пользователя")
    def user_delete(access_token):
        headers = {"Authorization": access_token}  # accessToken уже содержит "Bearer ..."
        return requests.delete(URL.USER_DELETE_ENDPOINT, headers=headers)