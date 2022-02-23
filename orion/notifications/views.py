from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Notification
from comments.models import Comment


@login_required(login_url=reverse_lazy('users:login'))
def get_notifications(request):
    notifications = Notification.objects.filter(status=Notification.NotificationStatus.UNREAD)
    comment_ids = [n.object_id for n in notifications.filter(content_type__model='comment')]
    comments = Comment.objects.filter(Q(id__in=comment_ids, parent__isnull=True, post__user=request.user) |
                                      Q(id__in=comment_ids, parent__user=request.user))
    response_comments = [{
            'username': comment.user.username,
            'avatar': comment.user.avatar.url,
            'post_id': comment.post.id,
            'text': comment.text,
            'created_at': comment.created_at,
        } for comment in comments[:3]
    ]
    return JsonResponse({'comments': response_comments, 'notifications_count': len(comments)})

