from django.urls import path

from store.views import store, cart, checkout, updateItem

app_name = 'store_app'

urlpatterns = [
	path('', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),

	path('update_item/', updateItem, name="update_item"),

]

