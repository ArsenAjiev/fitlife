from django.shortcuts import render, redirect
from community.models import *
from django.views.generic import ListView, CreateView
from community.forms import PostForm, AddCommentForm
from django.urls import reverse_lazy
from django.http import HttpResponse


def main_page(request):
    post = Post.objects.all().order_by('-created')
    context = {'post': post}
    return render(request, 'community/comm_main_page.html', context)


# tag index view
class TagIndexView(ListView):
    model = Post
    template_name = 'community/comm_main_page.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-created')


# post detail
def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    author = request.user
    # форма для добавления комментариев
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=author, post=post, text=form.cleaned_data["text"]
            )
            form = AddCommentForm()
            pass
    else:
        form = AddCommentForm()
    return render(request, 'community/post_detail.html', {'post': post, 'form': form})


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'community/create_post.html'
    success_url = reverse_lazy('community:main_page')
    raise_exception = True

    # добавляет в поле автор id текущего юзера автоматически
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(CreatePost, self).form_valid(form)


def delete_post(request, post_pk):
    # active_user = News.objects.get(author_id=request.user.pk)
    Post.objects.get(author_id=request.user.pk, id=post_pk).delete()
    return redirect('community:my_posts')


def my_posts(request):
    post = Post.objects.filter(author=request.user)
    context = {'post': post}
    return render(request, 'community/my_posts.html', context)


# удаление коментария по id. Может удалить только тот кто написал комментарий.
def delete_comment(request, comm_pk):
    author = request.user
    # получаем коментарий
    comment = Comment.objects.get(id=comm_pk)
    # получаем пост по ID через поле в связанной таблице (comment.post_id)
    object = Post.objects.get(id=comment.post_id)
    try:
        Comment.objects.get(id=comm_pk, author=author).delete()
    except:
        # если пост попытается удалить не автор, то возникнет исключение
        return HttpResponse("No permission")
    # Передавая объект; в качестве URL-а для перенаправления
    # будет использоваться результат вызова метода get_absolute_url()
    return redirect(object)



# # create post
# def create_post(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             #  logger.info(form.cleaned_data)
#             # unpacking the dictionary and assigning values from the received data to the model
#             # author=request.user - will be added automatically
#             Post.objects.create(**form.cleaned_data, author=request.user)
#             return redirect('community:main_page')
#
#     else:
#         form = PostForm()
#     post = 'qqq'
#     return render(request, 'community/create_post.html', {'post': post, 'form': form})

