
# fitlife

### Create directory and .gitignore file
```shell
### Create weather_app directory
     mkdir fitlife
     
     cd fitlife/

### Venv
   
```shell
# Create environment
python3.8 -m venv --copies venv

# Activate
source venv/bin/activate

# Make sure to use venv/bin/pip3.8 
which pip3.8

```


### Install packages
```shell
pip install Django

pip install psycopg2-binary

pip install gunicorn

```


### Create Django project in app directory


```shell
django-admin startproject app

```
     cd app/

```shell
python manage.py startapp store
```

### Create and install requirements.txt in app directory.

      
```shell
pip freeze > requirements.txt

pip install -r requirements.txt
```
###Run db migrations

```shell
python manage.py makemigrations
python manage.py migrate
```




### How to access environment variable values
      
```shell

(venv) my_pc....../fitlife$ python
Python 3.8.10 (default, Nov 26 2021, 20:14:08) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> print(os.environ['SECRET_KEY'])
django-insecure-i5dfie@d1m*%-$rlk^%d@!=tghm)qxt1hcck9q^zn0aa=+_y10

    Or you can see a list of all the environment variables using:
>>> os.environ


```

# Docker


```shell
# clear ALL data !!! 
docker system prune -a
docker volume prune

```
```shell
# show information 
docker ps -a
docker images
docker volume ls

```

### Run all at once

```shell
docker-compose up -d --build --force-recreate
```

```shell
docker-compose exec app python manage.py createsuperuser
```
--------------------------------------------------------
# Run server without docker (use sqlite)

### Create and install requirements.txt in app directory. 
```shell
pip install -r requirements.txt
```

###Run db migrations
```shell
python manage.py migrate
```
### Create superuser. 
```shell
python manage.py createsuperuser
```
```text
!!! IMPORTANT!!
Create  "Customer"  in admin interface (for superuser)
Create  "Membership"  in admin interface (for superuser)
```


### Create some products use management command
```shell
python manage.py create

```


Django-taggit 2.1.0
----
Run django-taggit 
```shell

pip install django-taggit

# необходим для работы со slug при переводе с кириллицы на латинские символы
pip install transliterate

```

### Add "taggit" to your INSTALLED_APPS

```text

INSTALLED_APPS = [
    ...
    'taggit',
    ...
]

```

```text
>>> apple = Food.objects.create(name="apple")
>>> apple.tags.add("red", "green", "delicious")
>>> apple.tags.all()
[<Tag: red>, <Tag: green>, <Tag: delicious>]
>>> apple.tags.remove("green")
>>> apple.tags.all()
[<Tag: red>, <Tag: delicious>]
>>> Food.objects.filter(tags__name__in=["red"])
[<Food: apple>, <Food: cherry>] 


```
   
```shell
python manage.py makemigrations
python manage.py migrate



```

### Create custom tag model in models.py
```text

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import re
from transliterate import slugify


class MyCustomTag(TagBase):
    # ... fields here

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    # ... methods (if any) here
    # переопределяю метод slugify
    def slugify(self, tag, i=None):
        # tag - <class 'str'>
        # преобразовываю <class 'str'> в <class 'list'>
        words = tag.split()
        # компилирую объекты регулярного выражения для последующего использования
        r1 = re.compile("[а-яА-Я]+")
        r2 = re.compile("[a-zA-Z]+")
        # ищу соответствие шаблону в начале строки и формирую два списка
        # слова написанные на кирилице и слова неаписанные латинскими символами.
        words_rus = [w for w in filter(r1.match, words)]
        words_eng = [w for w in filter(r2.match, words)]
        # преобразую список написанный на кирилице в латинские символы
        words_rus_to_eng = []
        for i in words_rus:
            words_rus_to_eng.append(slugify(i))
        # формирую окончательный список слов написанных латинскими символами
        words_final = words_eng + words_rus_to_eng
        # преобразовываю <class 'list'> в  <class 'str'>
        words_final_1 = ', '.join(words_final)
        slug = words_final_1
        return slug


class TaggedWhatever(GenericTaggedItemBase):
    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(
        MyCustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class Comment(models.Model):
    class Meta:
        ordering = ['-created']

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return self.text


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(through=TaggedWhatever)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('community:post_detail', kwargs={'post_pk': self.pk})



```

### !!! Задача - поместить в состав контекста каждого шаблона переменную, в которой хранится список тегов

```text
Можно создавать такую переменную в каждом контроллере, но это очень трудоемко.

```
### !!! Решение

```text
Объявим и зарегистрируем в проекте обработчик контекста, в котором и будет 
формироваться список тегов. 
Список тегов будет помещаться в переменную 'most_comm_tags' контекста шаблона.

```

```text
Создадим в пакете приложения модуль middlewares.py 
и запишем в него код обработчика контекста tags_context_processor(),

from community.models import Post

def tags_context_processor(request):
    context = {}
    context['most_comm_tags'] = Post.tags.most_common()[:10]
    return context
```

```text
В модуле settings.py пакета конфигурации зарегистрируем только что написанный обработчик контекста. 
Добавим имя этого обработчика в список context_processors из параметра options :
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 ...
                'community.middlewares.tags_context_processor',
            ],
        },
    },
]


```

```text
в модуле views.py пакета приложения объявим  контроллер-класс  TagIndexView:

def main_page(request):
    post = Post.objects.all()
    context = {'post': post}
    return render(request, 'community/comm_main_page.html', context)

# tag index view
class TagIndexView(ListView):
    model = Post
    template_name = 'community/comm_main_page.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-created')
```

```text
Context_object_name TagIndexView должно соответствовать имени переменной, 
которую вы повторяете в 'community/comm_main_page.html' — шаблон использует 'post',
 поэтому 'context_object_name' должно быть 'post'.
 
 Так как они ссылаются на одну и ту же страницу, и что бы на основании тегов формировать посты,
 context_object_name в двух зависимых контроллерах должны совпадать.

```

```text
Добавим в список маршрутов уровня приложения маршрут, ведущий на этот контроллер:

from django.urls import path
from community.views import *

app_name = 'community'

urlpatterns = [
    # главная страница fitlife community
    path('', main_page, name="main_page"),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='post_by_tag'),
    path('post_detail/<post_pk>/', post_detail, name='post_detail'),

```

```text
community/comm_main_page.html

    <div class="col-lg-2">
        <h1 class="h2 pb-4">Tags: </h1>

              {% for tag in most_comm_tags %}
              <a class="btn btn-outline-success" href="{% url 'community:post_by_tag' tag.slug %}" role="button">{{ tag.name }}</a>
               {% endfor %}

        <a  class="btn btn-outline-secondary" href="{% url 'community:main_page' %}"> Показать все посты </a>
        <button type="button" class="btn btn-outline-secondary" >Создать пост</button>
    </div>



```
### Update Tag
```text
решение проблемы изменения тегов при обновлении поста

```
```text

from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'tags']
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # важно при загрузке изображения!!!
            'image': forms.FileInput(attrs={'class': 'input-image-control'})
        }


```






# Test

```text
Что бы получать больше информации о тестах можно изменить значение параметра verbosity.
Доступными значениями для verbosity являются  0, 1 (значение по умолчанию), 2 и 3
```


```shell

python3 manage.py test --verbosity 2
python3 manage.py test -v 2

```

```shell

python3 manage.py test 
python3 manage.py test tests
python3 manage.py test tests.test_order -v 0

# путь до модуля membership/tests/test_model.py
python manage.py test membership.tests.test_model


```
