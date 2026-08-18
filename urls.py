# Адрес тестового стенда
BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Пути к ручкам
COURIER_PATH = "/api/v1/courier"                  # POST — создать, DELETE — удалить (+ /:id)
LOGIN_COURIER_PATH = "/api/v1/courier/login"      # POST  - залогиниться
ORDERS_PATH = "/api/v1/orders"                    # POST — создать заказ, GET — список заказов
ACCEPT_ORDER_PATH = "/api/v1/orders/accept"       # PUT, + /:id, courierId в параметрах - принять заказ
CANCEL_ORDER_PATH = "/api/v1/orders/cancel"       # PUT, track в параметрах track=*** - отменить заказ
GET_ORDER_BY_TRACK_PATH = "/api/v1/orders/track"  # GET, track в параметрах t=*** - получить заказ по треку

# Полные адреса
COURIER_URL = BASE_URL + COURIER_PATH
LOGIN_COURIER_URL = BASE_URL + LOGIN_COURIER_PATH
ORDERS_URL = BASE_URL + ORDERS_PATH
ACCEPT_ORDER_URL = BASE_URL + ACCEPT_ORDER_PATH
CANCEL_ORDER_URL = BASE_URL + CANCEL_ORDER_PATH
GET_ORDER_BY_TRACK_URL = BASE_URL + GET_ORDER_BY_TRACK_PATH
