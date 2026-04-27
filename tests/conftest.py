import pytest

from api_methods.user_methods import UserMethods
from helpers import (
    get_user_accesstoken,
    delete_user
)

#Фикстура только для очистки БД после теста
@pytest.fixture(scope="function")
def cleanup_user():
    token = None

    def register_for_cleanup(access_token):
        nonlocal token
        token = access_token
    
    yield register_for_cleanup
    
    if token:
        delete_user(token)