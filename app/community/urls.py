from django.urls import path

from community.views import *

app_name = 'community'

urlpatterns = [
    # главная страница fitlife community
    path('', main_page, name="main_page"),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='post_by_tag'),
    path('post_detail/<post_pk>/', post_detail, name='post_detail'),




    ]