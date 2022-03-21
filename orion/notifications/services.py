from typing import List, Union

from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet

from notifications.models import Notification


def set_notifications_status_as_read(notifications: Union[QuerySet, List[Notification]]) -> None:
    for notification in notifications:
        notification.status = Notification.NotificationStatus.READ
    Notification.objects.bulk_update(notifications, ['status'])


def get_unread_post_notifications(post_id: int) -> QuerySet:
    return Notification.objects.filter(
        content_type=ContentType.objects.get(model='post'),
        object_id=post_id,
        status=Notification.NotificationStatus.UNREAD,
    )
