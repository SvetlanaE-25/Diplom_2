import allure

from api_methods.user_methods import UserMethods
from api_methods.order_methods import OrderMethods
from helpers import (
    register_new_user_and_return_email_password,
    get_user_accesstoken,
    generate_random_list_ingredients
)
from data import ERROR_MESSAGES, INGREDIENT_HASHES

class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("Проверка создания заказа авторизованным пользователем с ингредиентами")
    def test_auth_user_create_order_with_ingredients(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()
        
        with allure.step("Авторизуемся и получаем токен пользователя для очистки БД после теста"):
            access_token = get_user_accesstoken(email, password, name)
            cleanup_user(access_token)

        with allure.step("Cоздаем заказ"):
            ingredients = generate_random_list_ingredients()
            response = OrderMethods.create_order(ingredients, access_token)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "order" in response.json()
            assert "number" in response.json()["order"]


    @allure.title("Создание заказа с авторизацией, но без ингредиентов")
    @allure.description("Проверка создания заказа авторизованным пользователем без ингредиентов")
    def test_auth_user_create_order_without_ingredients(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()
        
        with allure.step("Авторизуемся и получаем токен пользователя для очистки БД после теста"):
            access_token = get_user_accesstoken(email, password, name)
            cleanup_user(access_token)

        with allure.step("Cоздаем заказ без ингредиентов"):
            response = OrderMethods.create_order([], access_token)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 400
            assert response.json()["success"] == False

    
    @allure.title("Создание заказа без авторизации с ингредиентами возвращает ошибку")
    @allure.description("Проверка создания заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self):
        with allure.step("Создаём заказ без токена авторизации"):
            ingredients = generate_random_list_ingredients()
            response = OrderMethods.create_order(ingredients, token=None)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 500

    
    
    @allure.title("Создание заказа с авторизацией и неверным хешем ингредиентов возвращает ошибку")
    @allure.description("Проверка создания заказа с авторизацией и несуществующими ингредиентами")
    def test_create_order_with_auth_and_invalid_ingredients(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()
        
        with allure.step("Авторизуемся и получаем токен пользователя для очистки БД после теста"):
            access_token = get_user_accesstoken(email, password, name)
            cleanup_user(access_token)

        with allure.step("Создаём заказ с неверными хешами ингредиентов"):
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
            response = OrderMethods.create_order(invalid_ingredients, access_token)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 500



    @allure.title("Создание заказа без авторизации и с неверным хешем ингредиентов возвращает ошибку")
    @allure.description("Проверка создания заказа без авторизации с несуществующими ингредиентами")
    def test_create_order_without_auth_and_invalid_ingredients(self):
        with allure.step("Создаём заказ с неверными хешами без токена"):
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
            response = OrderMethods.create_order(invalid_ingredients, token=None)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 500
        