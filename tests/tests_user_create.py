import allure

from api_methods.user_methods import UserMethods
from data import ERROR_MESSAGES
from helpers import (
    generate_user_data,
    register_new_user_and_return_email_password
    )

class TestUserCreate:

    @allure.title("Создание пользователя с уникальными данными")
    @allure.description("Проверка создания пользователя с уникальными данными")
    def test_user_create_success(self, cleanup_user):
        with allure.step("Генерируем рандомные данные пользователя"):
            user_data = generate_user_data()
            email = user_data["email"]
            password = user_data["password"]
            name = user_data["name"]
        
        with allure.step("Регистрируем пользователя с полученными данными"):
            response = UserMethods.user_create(email, password, name)
        
        with allure.step("Запоминаем токен пользователя для очистки БД после теста"):
            access_token = response.json().get("accessToken")
            cleanup_user(access_token)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            assert response.json()["success"] == True
            assert response.json()["user"]["email"] == email
            assert response.json()["user"]["name"] == name
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

    

    @allure.title("Создание пользователя без email возвращает ошибку")
    @allure.description("Проверка создания пользователя без email")
    def test_user_create_without_email_error(self):
        with allure.step("Генерируем данные пользователя без email"):
            user_data = generate_user_data()
            user_data["email"] = ""
                    
        with allure.step("Отправляем запрос на создание пользователя с пустым полем email"):
            response = UserMethods.user_create(**user_data)
            
        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"
            assert response.json()["success"] == False
            assert response.json()["message"] == ERROR_MESSAGES["email_missing"]



    @allure.title("Создание пользователя без пароля возвращает ошибку")
    @allure.description("Проверка создания пользователя без пароля")
    def test_user_create_without_password_error(self):
        with allure.step("Генерируем данные пользователя без пароля"):
            user_data = generate_user_data()
            user_data["password"] = ""
        
        with allure.step("Отправляем запрос на создание пользователя с пустым полем Пароль"):
            response = UserMethods.user_create(**user_data)
            
        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"
            assert response.json()["success"] == False
            assert response.json()["message"] == ERROR_MESSAGES["password_missing"]


    @allure.title("Создание пользователя без имени возвращает ошибку")
    @allure.description("Проверка создания пользователя без имени")
    def test_user_create_without_name_error(self):
        with allure.step("Генерируем данные пользователя без имени"):
            user_data = generate_user_data()
            user_data["name"] = ""
        
        with allure.step("Отправляем запрос на создание пользователя с пустым полем Имя"):
            response = UserMethods.user_create(**user_data)
            
        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"
            assert response.json()["success"] == False
            assert response.json()["message"] == ERROR_MESSAGES["name_missing"]


    @allure.title("Создание дубликата пользователя возвращает ошибку")
    @allure.description("Проверка создания пользователя с повторяющимися данными")
    def test_duplicate_user_create_error(self, cleanup_user):
        with allure.step("Регистрируем нового пользователя"):
            email, password, name = register_new_user_and_return_email_password()

        with allure.step("Пытаемся создать пользователя с теми же данными"):
            response = UserMethods.user_create(email, password, name)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"
            assert response.json()["success"] == False
            assert response.json()["message"] == ERROR_MESSAGES["user_already_exists"]

        with allure.step("Получаем токен пользователя для очистки БД после теста"):
            login_response = UserMethods.user_login(email, password)
            access_token = login_response.json().get("accessToken")
            cleanup_user(access_token)