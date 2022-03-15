from django.urls import path

from store.views import store, cart, checkout

app_name = 'store_app'

urlpatterns = [
	path('', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),
]

