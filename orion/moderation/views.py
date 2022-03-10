from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from posts.models import Post


class PostModerationListView(ListView):
    model = Post
    template_name = 'moderation/posts_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.ArticleStatus.MODERATION)


@require_http_methods(['POST'])
def approve_post_publishing(request, post_id):
    # ToDo: implement access rules
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.ArticleStatus.ACTIVE
    return JsonResponse({'post_id': post_id}, status=200)
