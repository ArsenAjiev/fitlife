import shutil
import tempfile

from community.forms import AddCommentForm, PostForm
from community.models import Comment, Post

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from community.forms import PostForm


class TaskCreateFormTests(TestCase):

    def setUp(self):
        # создаем экземпляр пользователя
        self.client_1 = Client()
        self.user = User.objects.create_user(username='jalll', email='jacob@mail.qw', password='top_secret')
        self.client_1.force_login(self.user)


        # Создаем запись в базе данных
        Post.objects.create(
            author=self.user,
            title='title_1',
            text='Тестовый текст',
        )

    def test_post_create(self):
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        print("post_count", post_count)

        form_data = {
            'author': self.user,
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'tags': 'ddd'
        }

        response = self.client_1.post(
            reverse('community:create_post'),
            data=form_data,
            follow=True,
        )

        # Проверка редиректа
        self.assertRedirects(response, reverse('community:main_page'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count+1)