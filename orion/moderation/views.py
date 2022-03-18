from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.urls import reverse_lazy

from moderation.models import Moderation
from notifications.models import Notification
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
    moderation = Moderation(
        moderator=request.user,
        decision=Moderation.ModerationDecision.APPROVE,
        content_type=ContentType.objects.get(model='post'),
        object_id=post.id,
    )
    moderation.save()

    notifications = Notification.objects.filter(
        content_type=ContentType.objects.get(model='post'),
        object_id=post.id,
        status=Notification.NotificationStatus.UNREAD,
    )
    for notification in notifications:
        notification.status = Notification.NotificationStatus.READ
    Notification.objects.bulk_update(notifications, ['status'])

    Notification.create_notification(
        content_type=ContentType.objects.get(model='moderation'),
        object_id=moderation.id,
        user_id=request.user.id,
        target_user_id=post.user.id,
    )
    return JsonResponse({'post_id': post_id}, status=200)


@require_http_methods(['POST'])
@login_required(login_url=reverse_lazy('users:login'))
def decline_post_publishing(request, post_id):
    if not request.user.is_staff:
        raise PermissionDenied()
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.ArticleStatus.DECLINED
    post.save()

    moderation = Moderation(
        moderator=request.user,
        decision=Moderation.ModerationDecision.DECLINE,
        content_type=ContentType.objects.get(model='post'),
        object_id=post.id,
    )
    moderation.save()

    notifications = Notification.objects.filter(
        content_type=ContentType.objects.get(model='post'),
        object_id=post.id,
        status=Notification.NotificationStatus.UNREAD,
    )
    for notification in notifications:
        notification.status = Notification.NotificationStatus.READ
    Notification.objects.bulk_update(notifications, ['status'])

    Notification.create_notification(
        content_type=ContentType.objects.get(model='moderation'),
        object_id=moderation.id,
        user_id=request.user.id,
        target_user_id=post.user.id,
    )
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
