from django.urls import path

from store.views import *

app_name = 'store_app'

urlpatterns = [
    # главная страница магазина
    path('', store, name="store"),
    # страница, которая отображает содержимое страницы
    path('cart/', cart, name="cart"),
    # страница оформления заказа
    path('checkout/', checkout, name="checkout"),
    # ссылка на контроллер, который обрабатывает данные, полученные из функции "updateUserOrder" из файла cart.js
    path('update_item/', update_item, name="update_item"),
    #  ссылка на контроллер, который обрабатывает данные, полученные из функции "submitFormData" script checkout.html
    path('process_order/', process_order, name="process_order"),

]
