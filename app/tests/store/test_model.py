from django.test import TestCase, Client
from django.contrib.auth.models import User
from store.models import Customer, Product, Order, OrderItem, ShippingAddress


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Тестовый клиент – это класс Python, который умеет эмулировать запросы браузера.
        client = Client()
        # создаем экземпляр пользователя
        user = User.objects.create_user(username='jalll', email='jacob@mail.qw', password='top_secret')
        # Метод force_login() нужен, чтобы эмулировать авторизацию пользователя на сайте.
        # Используйте этот метод вместо login(), если необходимо авторизировать пользователя в тестах
        # и при этом не важен способ авторизации.
        client.force_login(user)

        Customer.objects.create(
            user_id=user.id,
            name='description',
            email='jacob@mail.qw'
        )

    def test_name_label(self):
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field('name').verbose_name
        print(field_label)
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_customer_name_is_str_name(self):
        customer = Customer.objects.get(id=1)
        expected_object_name = customer.name
        self.assertEquals(expected_object_name, str(customer))


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name='product_1',
            price=25,
            digital=False,
            image='/app/static-user/img/cart.png'
        )

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        print(field_label)
        self.assertEquals(field_label, 'name')

    def test_image_is_not_null(self):
        product = Product.objects.get(id=1)
        product.image = '/app/static-user/img/cart.png'
        print(product.image_url)
        self.assertEquals(product.image_url, '/media/app/static-user/img/cart.png')

    def test_image_is_null(self):
        product = Product.objects.get(id=1)
        product.image = None
        print(product.image_url)
        self.assertEquals(product.image_url, '')

    def test_product_name_is_str_name(self):
        product = Product.objects.get(id=1)
        expected_product_name = product.name
        self.assertEquals(expected_product_name, str(product))