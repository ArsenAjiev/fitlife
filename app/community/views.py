from django.shortcuts import render
from community.models import *
from django.views.generic import ListView

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


# post detail
def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    return render(request, 'community/post_detail.html', {'post': post})
