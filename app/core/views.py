from django.shortcuts import render, redirect
from store.models import *
from membership.models import Membership, Subscription
from store.utils import cart_data
from app.forms import UserRegisterForm
from django.contrib.auth import login



# Главная страница проекта
def index(request):
    # объект cartItems нужен для отображения количества товаров в корзине на главной странице
    data = cart_data(request)
    cart_items = data['cart_items']
    subscription = Subscription.objects.all()[:3]
    context = {
        "cart_items": cart_items,
        "subscription": subscription
    }
    return render(request, 'core/index.html', context)



# информация о сайте
def about(request):
    # объект cartItems нужен для отображения количества товаров в корзине на главной странице
    data = cart_data(request)
    cart_items = data['cart_items']
    context = {"cart_items": cart_items}
    return render(request, 'core/about.html', context)


# контакты
def contact(request):
    # объект cartItems нужен для отображения количества товаров в корзине на главной странице
    data = cart_data(request)
    cart_items = data['cart_items']
    context = {"cart_items": cart_items}
    return render(request, 'core/contact.html', context)


# тарифы
def tariffs(request):
    # объект cartItems нужен для отображения количества товаров в корзине на главной странице
    data = cart_data(request)
    cart_items = data['cart_items']
    subscription = Subscription.objects.all()
    context = {
        "cart_items": cart_items,
        "subscription": subscription

    }
    return render(request, 'core/tariffs.html', context)


def profile(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')
    items = OrderItem.objects.filter(order__customer=customer)

    context = {'order': order, 'cart_items': cart_items, 'items': items}
    return render(request, 'core/profile.html', context)


# регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # одновременное автоматическое создание объекта Customer, для совершения покупок
            Customer.objects.create(user=request.user,
                                    name=form.cleaned_data.get('username'),
                                    email=form.cleaned_data.get('email'))
            Membership.objects.create(user=request.user,
                                      name=form.cleaned_data.get('username'),
                                      email=form.cleaned_data.get('email'))

            return redirect('core:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
