import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy

from .models import Notification
from comments.models import Comment
from notifications.models import Notification


@login_required(login_url=reverse_lazy('users:login'))
def get_notifications(request):
    comment_ids = Notification.objects.filter(
        target_user=request.user,
        status=Notification.NotificationStatus.UNREAD,
        content_type__model='comment').values_list('object_id')
    comments = Comment.objects.filter(id__in=comment_ids,).order_by('-modified_at')

    response_comments = [{
            'user_id': comment.user.id,
            'username': comment.user.username,
            'avatar': comment.user.avatar.url,
            'post_id': comment.post.id,
            'post_slug': comment.post.slug,
            'text': comment.text,
            'created_at': comment.created_at,
            'comment_id': comment.id,
        } for comment in comments[:3]
    ]
    return JsonResponse({'comments': response_comments,
                         'notifications_count': len(comments),
                         'current_user_id': request.user.id})


@require_http_methods(["POST"])
@login_required(login_url=reverse_lazy('users:login'))
def mark_as_read(request):
    post_data = json.loads(request.body.decode("utf-8"))
    ids = post_data.get('ids')
    notifications = Notification.objects.filter(object_id__in=ids)
    Notification.mark_notifications_read(notifications)
    return JsonResponse({'ids': ids})


@require_http_methods(["GET"])
@login_required(login_url=reverse_lazy('users:login'))
def mark_as_read_and_redirect(request, object_id):
    notification = get_object_or_404(Notification, object_id=object_id)
    if notification.content_type.model == 'comment':
        Notification.mark_notifications_read([notification])
        comment = get_object_or_404(Comment, pk=notification.object_id)
        slug = comment.post.slug
        return redirect(reverse('posts:detail', kwargs={'slug': slug}) + f'#comment-{comment.id}')
