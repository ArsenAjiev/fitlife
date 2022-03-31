from django.urls import path

from community.views import *

app_name = 'community'

urlpatterns = [
    # главная страница fitlife community
    path('', main_page, name="main_page"),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='post_by_tag'),
    path('post_detail/<post_pk>/', post_detail, name='post_detail'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
    path('my_posts/', my_posts, name='my_posts'),
    path('delete_comment/<comm_pk>/', delete_comment, name='delete_comment'),
    path('delete_post/<post_pk>/', delete_post, name='delete_post'),

    ]