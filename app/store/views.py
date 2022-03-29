from django.shortcuts import render, get_object_or_404
from store.models import *
from django.http import JsonResponse
import json
import datetime
from store.utils import cart_data, guest_order


def store(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context = {'products': products, "cart_items": cart_items}
    return render(request, 'store/store.html', context)


def cart(request):

    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'store/checkout.html', context)


# Получаем данные из функции JS updateUserOrder.
# Если нет экземпляра модели 'Order', то создается новый.
# На основе полученных данных создаем экземпляры модели 'OrderItem'.
def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # изменение значений в поле 'quantity' модели 'OrderItem'
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added!', safe=False)


# Получаем данные из функции JS submitFormData.
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    print('Data', request.body)
    print(transaction_id)

    return JsonResponse('Payment complete', safe=False)


def my_orders(request, order_id):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=True)
    items = OrderItem.objects.filter(order__customer=customer)

    order_item = get_object_or_404(Order, pk=order_id, customer=customer)
    context = {'order_item': order_item, 'order': order, 'cart_items': cart_items, 'items': items}
    return render(request, 'store/my_orders.html', context)


def purchase_archive(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=True).order_by('-date_ordered')
    items = OrderItem.objects.filter(order__customer=customer)

    context = {'order': order, 'cart_items': cart_items, 'items': items}
    return render(request, 'store/purchase_archive.html', context)