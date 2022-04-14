import shutil
import tempfile

from django.test import Client, TestCase, override_settings
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User

from community.models import Comment, Post
from community.forms import PostForm, AddCommentForm



# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоваться
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(""" setUpClass for Post""")
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        print(""" tearDownClass for Post""")
        super().tearDownClass()
        # Модуль shutil - библиотека Python с прекрасными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        print(""" setUp for Post""")
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

    # проверка валидности формы PostForm
    def test_post_form_with_valid_data(self):
        print('1. Test name: test_post_form_with_valid_data - start')
        # Подготавливаем данные для передачи в форму - изображение
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form = PostForm(data={
            'title': 'test title',
            'text': 'Тестовый текст',
            'tags': 'ddd qwe, tyu',
            'image': uploaded
        })
        print('1. Test name: test_post_form_with_valid_data - finish')
        self.assertTrue(form.is_valid())

    # проверка создания поста через форму PostForm
    def test_post_create(self):
        print('2. Test name: test_post_create - start')
        # Подсчитаем количество записей в Post
        post_count = Post.objects.count()
        print("post_count", post_count)
        # Подготавливаем данные для передачи в форму - изображение
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'tags': 'ddd, jjj, ccc',
            'image': uploaded
        }

        response = self.client_1.post(
            reverse('community:create_post'),
            data=form_data,
            follow=True,
        )
        saved_post = Post.objects.last()
        # проверяем, что сохраненные значения соответствуют тем значениям, которые передали в форму
        print('author', saved_post.author)
        print('title', saved_post.title)
        print('text', saved_post.text)
        print('tags', [item.name for item in saved_post.tags.all()])
        print('image', saved_post.image.url)
        print('2. Test name: test_post_create - finish')
        # Проверка редиректа
        self.assertRedirects(response, reverse('community:main_page'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count+1)


class CommentCreateFormTests(TestCase):

    def setUp(self):
        print(""" setUp for Comment""")
        # создаем экземпляр пользователя
        self.client_1 = Client()
        self.user = User.objects.create_user(username='jalll', email='jacob@mail.qw', password='top_secret')
        self.client_1.force_login(self.user)

        # Создаем запись в базе данных
        self.post = Post.objects.create(
            author=self.user,
            title='title_1',
            text='Тестовый текст',
        )
        # Создаем запись в базе данных
        Comment.objects.create(
            author=self.user,
            text='Тестовый текст',
            post=self.post,
        )

    # проверка валидности формы PostForm
    def test_comment_form_with_valid_data(self):
        print('3. Test name: test_comment_form_with_valid_data - start')
        form = AddCommentForm(data={
            'author': self.user,
            'text': 'Тестовый текст',
            'post': self.post,
        })
        print('3. Test name: test_comment_form_with_valid_data - finish')
        self.assertTrue(form.is_valid())

    # проверка создания поста через форму PostForm
    def test_comment_create(self):
        print('4. Test name: test_comment_create - start')
        # Подсчитаем количество записей в Post
        comment_count = Comment.objects.count()
        print("comment_count", comment_count)

        form_data = {
            'author': self.user,
            'text': 'Тестовый текст',
            'post': self.post,
        }

        response = self.client_1.post(
            reverse('community:post_detail', kwargs={'post_pk': 1}),
            data=form_data,
            follow=True,
        )
        saved_comment = Comment.objects.last()
        # проверяем, что сохраненные значения соответствуют тем значениям, которые передали в форму
        print('author', saved_comment.author)
        print('text', saved_comment.text)
        print('post', saved_comment.post)
        # Проверим, что ничего не упало и страница отдаёт код 200
        print('Test name: response.status_code', response.status_code)
        self.assertEqual(response.status_code, 200)
        print('4. Test name: test_post_create - finish')
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Comment.objects.count(), comment_count+1)

