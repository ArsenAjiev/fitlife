from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from community.forms import AddCommentForm


class AddCommentFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = AddCommentForm()
        # print(form.fields['text'].label)
        self.assertTrue(form.fields['text'].label == 'Введите комментарий')


    # def test_comment(self):
    #     comment = 123
    #     form_data = {'text': comment}
    #     print(form_data)
    #     form = AddCommentForm(data=form_data)
    #     self.assertTrue(form.is_valid())
