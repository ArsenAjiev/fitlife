from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class CoreTestClass(TestCase):

    def test_register_user(self):
        client_1 = Client()
        data = {
            "username": 'test_user1',
            "first_name": 'first_name_user',
            "last_name": 'last_name_user',
            "email": 'email@mail.com',
            "password1": 'AA123dfggs23',
            "password2": 'AA123dfggs23'
        }
        # response = client_1.post(reverse('register'), data=data)
        response = client_1.post("/accounts/register/", data=data)
        print("test_register_user status_code: ", response.status_code)
        current_user = User.objects.first()
        print("test_register_user current_user: ", current_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
        self.assertTrue(User.objects.exists())

    def test_index_page_view(self):
        client_1 = Client()
        response = client_1.get(reverse('core:index'))
        print("test_index_page_view status_code: ", response.status_code)
        self.assertEqual(response.status_code, 200)
        # доступные объекты
        # print(dir(response))

    def test_about_page_view(self):
        client_1 = Client()
        response = client_1.get(reverse('core:about'))
        print("test_about_page_view status_code :", response.status_code)
        self.assertEqual(response.status_code, 200)
        # доступные объекты
        # print(dir(response))

    def test_contact_page_view(self):
        client_1 = Client()
        response = client_1.get(reverse('core:contact'))
        print("test_contact_page_view status_code :", response.status_code)
        self.assertEqual(response.status_code, 200)
        # доступные объекты
        # print(dir(response))

    def test_tariffs_page_view(self):
        client_1 = Client()
        response = client_1.get(reverse('core:tariffs'))
        print("test_tariffs_page_view status_code :", response.status_code)
        self.assertEqual(response.status_code, 200)
        # доступные объекты
        # print(dir(response))

