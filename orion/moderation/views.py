from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse_lazy

from moderation.models import Moderation
from moderation.services import post_moderation_run_action
from posts.models import Post
from posts.services import post_status_update


class PostModerationListView(PermissionRequiredMixin, ListView):
    model = Post
    template_name = 'moderation/posts_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(status=Post.ArticleStatus.MODERATION)
    login_url = reverse_lazy('users:login')

    def has_permission(self):
        return self.request.user.is_staff


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def approve_post_publishing(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = post_status_update(post_id, Post.ArticleStatus.ACTIVE)
    post_moderation_run_action(request.user, post, Moderation.ModerationDecision.APPROVE)
    return JsonResponse({'post_id': post_id}, status=200)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def decline_post_publishing(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = post_status_update(post_id, Post.ArticleStatus.DECLINED)
    post_moderation_run_action(request.user, post, Moderation.ModerationDecision.DECLINE)
    return JsonResponse({'post_id': post_id}, status=200)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def ban_post(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post_status_update(post_id, Post.ArticleStatus.BANNED)
    return JsonResponse({'post_id': post_id}, status=200)
