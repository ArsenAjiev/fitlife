import json
from store.models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    # print('cart_view', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']
    for i in cart:
        try:
            cart_items += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.image_url
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        # print(customer)
    else:
        cookieData = cookie_cart(request)
        cart_items = cookieData['cart_items']
        order = cookieData['order']
        items = cookieData['items']

    return {'cart_items': cart_items, 'order': order, 'items': items}


def guest_order(request, data):
    print('User is not logged in...')
    print("cookie", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieDate = cookie_cart(request)
    items = cookieDate['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
