from django.views.generic import ListView

from posts.models import Post


class PostModerationListView(ListView):
    model = Post
    template_name = 'moderation/posts_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.ArticleStatus.MODERATION)
