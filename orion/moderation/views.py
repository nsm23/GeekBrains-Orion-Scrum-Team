from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse_lazy

from posts.models import Post


class PostModerationListView(ListView):
    model = Post
    template_name = 'moderation/posts_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.ArticleStatus.MODERATION)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def approve_post_publishing(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.ArticleStatus.ACTIVE
    post.save()
    return JsonResponse({'post_id': post_id}, status=200)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def decline_post_publishing(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.ArticleStatus.DECLINED
    post.save()
    return JsonResponse({'post_id': post_id}, status=200)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def ban_post(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.ArticleStatus.BANNED
    post.save()
    return JsonResponse({'post_id': post_id}, status=200)
