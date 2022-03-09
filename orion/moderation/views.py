from django.views.generic import ListView

from posts.models import Post


class PostModerationListView(ListView):
    model = Post
    template_name = 'moderation/posts_list.html'
