from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import re


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



