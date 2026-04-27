import allure

from api_methods.user_methods import UserMethods
from data import ERROR_MESSAGES
from helpers import register_new_user_and_return_email_password, get_user_accesstoken


class TestUserLogin:

    @allure.title("Вход пользователя с уникальными данными")
    @allure.description("Проверка входа пользователя с уникальными данными")
    def test_user_login_success(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()
        
        with allure.step("Выполняем вход с email и паролем"):
            response = UserMethods.user_login(email, password)

        with allure.step("Запоминаем токен пользователя для очистки БД после теста"):
            access_token = response.json().get("accessToken")
            cleanup_user(access_token)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()
            assert response.json()["user"]["email"] == email
            assert response.json()["user"]["name"] == name

    

    
    @allure.title("Вход пользователя с неверными email")
    @allure.description("Проверка ошибки при входе пользователя без с неверным email")
    def test_login_wrong_email(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()

        with allure.step("Получаем токен для очистки БД"):
            access_token = get_user_accesstoken(email, password, name)
            cleanup_user(access_token)
        
        with allure.step("Выполняем вход с неверным email"):
            response = UserMethods.user_login("wrong_email", password)
        
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == ERROR_MESSAGES["email_incorrect"]

        


    @allure.title("Вход пользователя с неверными паролем")
    @allure.description("Проверка ошибки при входе пользователя без с неверным паролем")
    def test_login_wrong_password(self, cleanup_user):
        with allure.step("Регистриуем пользователя и возвращаем его данные для входа"):
            email, password, name = register_new_user_and_return_email_password()
        
        with allure.step("Получаем токен для очистки БД"):
            access_token = get_user_accesstoken(email, password, name)
            cleanup_user(access_token)
        
        with allure.step("Выполняем вход с неверным паролем"):
            response = UserMethods.user_login(email, "wrong_password")
        
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == ERROR_MESSAGES["password_incorrect"]


        
