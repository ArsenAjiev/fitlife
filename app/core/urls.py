
from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [

    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('profile/', profile, name='profile'),
    path('tariffs/', tariffs, name='tariffs'),

]
