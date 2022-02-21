from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from comments.models import Comment
from .models import Notification


@login_required(login_url=reverse_lazy('users:login'))
def get_notifications(request, content_type: str):
    notifications = Notification.objects.all()  # filter(content_type__model=content_type)
    if content_type == 'comment':
        # comments = Comment.objects.filter()
        response = [{'id': n.id, 'content_type': n.content_type.model, 'status': n.status, }
                         for n in notifications]
        return JsonResponse({'notifications': response})
    return JsonResponse({'detail': 'Unknown content_type'}, status=404)
