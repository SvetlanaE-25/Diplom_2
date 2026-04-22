#Вспомогательные функции для тестов

import requests
import random
import string
from api_methods.user_methods import UserMethods
from api_methods.order_methods import OrderMethods
from data import INGREDIENT_HASHES

#Функция генерирует случайную строку из букв нижнего регистра
def generate_random_string(length=10): 
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


#Функция генерирует рандомные данные пользователя
def generate_user_data():
    email = generate_random_string(10) + "@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)
    return {
        "email": email,
        "password": password,
        "name": name
    }


#Функция генерирует данные пользователя без email
def generate_user_data_without_email():
    email = ""
    password = generate_random_string(10)
    name = generate_random_string(10)
    return {
        "email": email,
        "password": password,
        "name": name
    }


#Функция генерирует данные пользователя без пароля
def generate_user_data_without_password():
    email = generate_random_string(10)
    password = ""
    name = generate_random_string(10)
    return {
        "email": email,
        "password": password,
        "name": name
    }


#Функция генерирует данные пользователя без имени
def generate_user_data_without_name():
    email = generate_random_string(10)
    password = generate_random_string(10)
    name = ""
    return {
        "email": email,
        "password": password,
        "name": name
    }


#Функция регистрирует нового пользователя и возвращает его данные
def register_new_user_and_return_email_password():
    email = generate_random_string(10) + "@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)
    response = UserMethods.user_create(email, password, name)
    if response.status_code == 200 and response.json()["success"] is True:
        return email, password, name
    return None, None, None

#Получение токена пользователя
def get_user_accesstoken(email, password, name):
    response = UserMethods.user_login(email, password)
    if response.status_code == 200:
        return response.json().get("accessToken")
    return None


#Удаление пользователя по токену
def delete_user(access_token):
    return UserMethods.user_delete(access_token)


#Функция генерирует случайный список ингредиентов
def generate_random_list_ingredients():
    valid_ingredients = INGREDIENT_HASHES["valid_hash"]
    return random.sample(valid_ingredients, min(2, len(valid_ingredients)))