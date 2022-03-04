from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hub.models import Hub
from django.utils.translation import gettext_lazy as _

from likes.models import LikeDislike
from users.models import User


class Post(models.Model):

    class ArticleStatus(models.TextChoices):
        DRAFT = 'DRAFT', _('DRAFT'),
        ACTIVE = 'ACTIVE', _('ACTIVE'),
        MODERATION = 'ON MODERATION', _('ON MODERATION')
        DELETED = 'DELETED', _('DELETED')

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Элиас для урла')
    text = models.TextField(verbose_name='Полный текст')
    brief_text = models.TextField(verbose_name='Сокращенный текст для списков')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='posts', verbose_name='Автор')
    hub = models.ForeignKey(Hub, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts', verbose_name='Хаб')
    image = models.ImageField(upload_to='posts', null=True, blank=True, verbose_name='Картинка поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    status = models.CharField(choices=ArticleStatus.choices, max_length=16, default=ArticleStatus.ACTIVE)
    votes = GenericRelation(LikeDislike, related_query_name='posts')

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ('-created_at',)
