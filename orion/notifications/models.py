from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):

    class NotificationStatus(models.TextChoices):
        UNREAD = 'UNREAD', _('UNREAD'),
        READ = 'READ', _('READ'),

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.CharField(max_length=8, choices=NotificationStatus.choices, default=NotificationStatus.UNREAD)

    def __str__(self):
        return f'notification of {self.content_object} {self.object_id}'
