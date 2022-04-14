from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.urls import reverse

from community.models import Post


class CommunityViewSet(TestCase):

    def setUp(self):
        print(""" setUp for view""")
        # создаем экземпляр пользователя
        self.client_1 = Client()
        self.user = User.objects.create_user(username='jalll', email='jacob@mail.qw', password='top_secret')
        self.client_1.force_login(self.user)

    def test_main_page_view(self):
        print('1. Test name: test_main_page_view - start')
        response = self.client_1.get(reverse('community:main_page'))
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        # доступные объекты
        # print(dir(response))
        # print(response.content.decode())
        # print(response.context)
        # print(type(response.context))
        print('1. Test name: test_main_page_view - finish')

    def test_post_by_tag_view(self):
        Post.objects.create(
            author=self.user,
            title='title_1',
            text='Тестовый текст',
        )
        # создаем пост
        post_1 = Post.objects.get(pk=1)
        # добавляем теги
        post_1.tags.add("red", "green", "delicious")
        # print('tags :', [item.name for item in post_1.tags.all()])
        print('2. Test name: test_post_by_tag_view - start')
        response = self.client_1.get(reverse('community:post_by_tag', kwargs={'tag_slug': 'red'}))
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        # print(dir(response))
        # print(response.context_data)
        # print(response.context['post'])

        # получаем экземпляр post_1, где title='title_1' по тегу 'red'
        print([item.title for item in response.context['post']])
        print('2. Test name: test_post_by_tag_view - finish')

    def test_post_detail(self):
        Post.objects.create(
            author=self.user,
            title='title_1_post_detail',
            text='Тестовый текст',
        )
        # создаем пост
        post_1 = Post.objects.get(pk=1)
        # добавляем теги
        post_1.tags.add("red", "green", "delicious")
        print('3. Test name: test_get_queryset - start')
        response = self.client_1.get(reverse('community:post_detail', kwargs={'post_pk': 1}))
        # print(response.status_code)

        # получаем экземпляр post_1, где title='title_1_post_detail' по 'post_pk=1'
        print(response.context['post'])
        # print(response.context)
        self.assertEqual(response.status_code, 200)
        print('3. Test name: test_get_queryset - finish')

    # проверка обновления поста
    def test_post_update(self):
        Post.objects.create(
            author=self.user,
            title='title_1',
            text='Тестовый текст',
        )
        # создаем пост
        post_1 = Post.objects.get(pk=1)
        # добавляем теги
        post_1.tags.add("red", "green", "delicious")

        print('4. Test name: test_post_update - start')
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        print("post_count", post_count)

        form_data = {
            'title': 'Обновленный текст заголовок',
            'text': 'Тестовый текст',
            'tags': 'новый, jjj, ccc',
        }

        response = self.client_1.post(
            reverse('community:edit_post', kwargs={'pk': 1}),
            data=form_data,
            follow=True,
        )
        updated_post = Post.objects.last()
        # проверяем, что сохраненные значения соответствуют тем значениям, которые передали в форму
        print('author', updated_post.author)
        print('title', updated_post.title)
        print('text', updated_post.text)
        print('tags', [item.name for item in updated_post.tags.all()])

        print('4. Test name: test_post_update - finish')
        # Проверка редиректа
        self.assertRedirects(response, reverse('community:main_page'))
        # Проверяем, число постов не увеличилось
        self.assertEqual(Post.objects.count(), post_count)
