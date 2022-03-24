from django.shortcuts import render, redirect
from store.models import *
from store.utils import cart_data
from app.forms import UserRegisterForm
from django.contrib.auth import login


# Главная страница проекта
def index(request):
    # объект cartItems нужен для отображения количества товаров на главной странице
    data = cart_data(request)
    cartItems = data['cartItems']
    context = {"cartItems": cartItems}
    return render(request, 'index.html', context)


# регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # одновременное создание объекта Customer, для совершения покупок
            Customer.objects.create(user=request.user,
                                    name=form.cleaned_data.get('username'),
                                    email=form.cleaned_data.get('email'))
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# информация о сайте
def about(request):
    # объект cartItems нужен для отображения количества товаров на главной странице
    data = cart_data(request)
    cartItems = data['cartItems']
    context = {"cartItems": cartItems}
    return render(request, 'about.html', context)


def profile(request):
    data = cart_data(request)
    cartItems = data['cartItems']

    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=True)
    items = OrderItem.objects.filter(order__customer=customer)


    context = { 'order': order, 'cartItems': cartItems, 'items': items}
    return render(request, 'profile.html', context)

