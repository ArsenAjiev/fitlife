from community.models import Post


def tags_context_processor(request):
    context = {}
    context['most_comm_tags'] = Post.tags.most_common()[:15]
    return context
