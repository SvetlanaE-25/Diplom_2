class URL:

    BASE_URL = "https://stellarburgers.education-services.ru/"

    # Эндпоинты для пользователя
    USER_REGISTRATION_ENDPOINT = f"{BASE_URL}/api/auth/register"
    USER_LOGIN_ENDPOINT = f"{BASE_URL}/api/auth/login"
    USER_DELETE_ENDPOINT = f"{BASE_URL}//api/auth/user"

    # Эндпоинты для заказов
    CREATE_ORDER_ENDPOINT = f"{BASE_URL}/api/orders"
    INGREDIENTS_DATA_ENDPOINT = f"{BASE_URL}/api/ingredients"