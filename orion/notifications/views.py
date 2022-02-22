from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Notification


@login_required(login_url=reverse_lazy('users:login'))
def get_notifications(request, content_type: str):
    notifications = Notification.objects.filter(content_type__model=content_type)
    if content_type == 'comment':
        response = []
        for notification in notifications:
            comment = notification.content_type.get_object_for_this_type(id=notification.object_id)
            # if comment.parent:
            response_item = {
                'username': comment.user.username,
                'avatar': comment.user.avatar.url,
                'post_id': comment.post.id,
                'text': comment.text,
            }
            response.append(response_item)
        return JsonResponse({'notifications': response})
    return JsonResponse({'detail': 'Unknown content_type'}, status=404)
