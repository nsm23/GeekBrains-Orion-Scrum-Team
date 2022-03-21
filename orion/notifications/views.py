import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse, reverse_lazy

from comments.models import Comment
from likes.models import LikeDislike
from moderation.models import Moderation
from notifications.models import Notification
from posts.models import Post

COMMENT_NOTIFICATIONS_NUMBER_TO_SHOW = 3
LIKES_NOTIFICATIONS_NUMBER_TO_SHOW = 3
POST_TO_MODERATOR_NUMBER_TO_SHOW = 3
POST_MODERATION_RESULT_NUMBER_TO_SHOW = 3


from typing import List, Union
from django.db.models import QuerySet

def get_notifying_object(notifications: Union[QuerySet, List[Notification]],
                         model,
                         order_by: Union[str, None] = None) -> QuerySet:
    object_ids = notifications.filter(content_type__model=model.__name__.lower()).values_list('object_id')
    queryset = model.objects.filter(id__in=object_ids)
    if order_by:
        queryset = queryset.order_by(order_by)
    return queryset


@login_required(login_url=reverse_lazy('users:login'))
def get_notifications(request):
    notifications = Notification.objects.filter(
        target_user=request.user,
        status=Notification.NotificationStatus.UNREAD,
    )

    comments = get_notifying_object(notifications, Comment, '-modified_at')
    likes = get_notifying_object(notifications, LikeDislike)
    moderation_acts = get_notifying_object(notifications, Moderation, '-date')

    response_notifications = {}
    if request.user.is_staff:
        post_ids = Notification.objects.filter(
            target_user__isnull=True,
            status=Notification.NotificationStatus.UNREAD,
            content_type__model='post',
        ).values_list('object_id')
        posts_to_moderate = Post.objects.filter(id__in=post_ids)
        response_posts_to_moderate = [{
            'post_id': post.id,
            'post_slug': post.slug,
            'post_title': post.title,
            'post_user_id': post.user.id,
            'username': post.user.username,
            'user_avatar_url': post.user.avatar.url,
        } for post in posts_to_moderate[:POST_TO_MODERATOR_NUMBER_TO_SHOW]]
        response_notifications = {
            'posts_to_moderate': response_posts_to_moderate,
            'posts_to_moderate_count': len(post_ids)
        }

    response_comments = [{
            'user_id': comment.user.id,
            'username': comment.user.username,
            'user_avatar_url': comment.user.avatar.url,
            'post_id': comment.post.id,
            'text': comment.text,
            'created_at': comment.created_at,
            'comment_id': comment.id,
        } for comment in comments[:COMMENT_NOTIFICATIONS_NUMBER_TO_SHOW]
    ]
    response_likes = [{
            'user_id': like.user.id,
            'username': like.user.username,
            'user_avatar_url': like.user.avatar.url,
            'like_id': like.id,
            'vote': like.vote,
            'post_id': like.object_id,
            'post_title': like.content_object.title,
        } for like in likes[:LIKES_NOTIFICATIONS_NUMBER_TO_SHOW]
    ]
    response_moderations = [{
            'object_id': mod.object_id,
            'content_type': mod.content_type.model,
            'decision': mod.decision,
            'comment': mod.comment,
            'text': mod.content_object.title if mod.content_type.model == 'post' else '',
        } for mod in moderation_acts[:POST_TO_MODERATOR_NUMBER_TO_SHOW]]
    return JsonResponse(dict({
        'comments': response_comments,
        'likes': response_likes,
        'moderation_acts': response_moderations,
        'notifications_count': len(comments) + len(likes) + len(moderation_acts),
        'current_user_id': request.user.id
    }, **response_notifications))


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
def mark_as_read_and_redirect(request, object_id, object_model):
    notification = Notification.objects.filter(object_id=object_id, content_type__model=object_model)
    Notification.mark_notifications_read(notification)
    if object_model == 'comment':
        comment = get_object_or_404(Comment, pk=object_id)
        slug = comment.post.slug
        return redirect(reverse('posts:detail', kwargs={'slug': slug}) + f'#comment-{comment.id}')
    if object_model == 'likedislike':
        like = get_object_or_404(LikeDislike, pk=object_id)
        return redirect(reverse('posts:detail', kwargs={'slug': like.content_object.slug}))
    if object_model == 'post':
        post = get_object_or_404(Post, pk=object_id)
        return redirect(reverse('posts:detail', kwargs={'slug': post.slug}))
    raise Http404
