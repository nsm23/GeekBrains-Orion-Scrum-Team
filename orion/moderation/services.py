from django.contrib.contenttypes.models import ContentType

from .models import Moderation
from notifications.models import Notification
from notifications import services as notif_services
from posts.models import Post
from users.models import User


def post_moderation_run_action(user: User, post: Post,
                               decision: Moderation.ModerationDecision) -> Moderation:
    moderation = Moderation(
        moderator_id=user.id,
        decision=decision,
        content_type=ContentType.objects.get(model='post'),
        object_id=post.id,
    )
    moderation.save()

    notif_services.set_notifications_status_as_read(
        notif_services.get_unread_post_notifications(post.id))

    Notification.create_notification(
        content_type=ContentType.objects.get(model='moderation'),
        object_id=moderation.id,
        user_id=user.id,
        target_user_id=post.user.id,
    )
    return moderation
