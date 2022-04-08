from django.urls import path
from membership.views import *

app_name = 'membership'

urlpatterns = [

    # path('', index, name='index'),
    path('my_subscription/', my_subscription, name='my_subscription'),
    path('tariffs/', tariffs, name='tariffs'),
    path('add_membership/<item_pk>/', add_membership, name='add_membership'),
    path('activation/<item_pk>/', activation, name='activation'),
    # path('deactivation/<item_pk>/', deactivation, name='deactivation'),
    path('delete_membership/<item_pk>/', delete_membership, name='delete_membership'),
    path('check_visit/<item_pk>/', check_visit, name='check_visit'),
]
